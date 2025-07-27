"""
O3-Powered Query Decomposer for Financial Analysis
Uses OpenAI's o3 reasoning model to iteratively decompose queries and interact with MCP server
"""

import asyncio
import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import openai
from pydantic import BaseModel, Field

from .yfinance_client import YFinanceClient, FinanceToolRegistry, FinanceResponse


@dataclass
class DecompositionStep:
    step_id: str
    description: str
    step_type: str  # "DATA", "ANALYSIS", "OUTPUT"
    tool_name: Optional[str] = None  # For DATA: yfinance tool name
    parameters: Optional[Dict[str, Any]] = None  # For DATA: tool parameters
    analysis_prompt: Optional[str] = None  # For ANALYSIS: GPT-4o prompt
    output_template: Optional[str] = None  # For OUTPUT: formatting instructions
    depends_on: List[str] = None
    status: str = "pending"
    result: Any = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.depends_on is None:
            self.depends_on = []
        if self.parameters is None:
            self.parameters = {}


@dataclass
class QueryDecomposition:
    """Complete query decomposition with iterative refinement"""
    query: str
    steps: List[DecompositionStep]
    reasoning: str
    final_analysis: Optional[str] = None
    status: str = "in_progress"  # in_progress, completed, failed


class O3QueryDecomposer:
    """
    Advanced query decomposer using OpenAI's o3 reasoning model
    Iteratively refines decomposition based on available data from MCP server
    """
    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.openai_client = openai.AsyncOpenAI(api_key=openai_api_key)
        self.finance_client = None
        self.current_query = None  # Store current query for context
        
    async def __aenter__(self):
        self.finance_client = YFinanceClient()
        await self.finance_client.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.finance_client:
            await self.finance_client.__aexit__(exc_type, exc_val, exc_tb)

    async def decompose_query(self, user_query: str, debug_mode: bool = False) -> QueryDecomposition:
        """
        Main entry point: decompose a user query into executable steps
        Uses iterative refinement with o3 reasoning
        """
        self.current_query = user_query  # Store for context in output formatting
        print(f"\n🧠 O3 Reasoning: Starting query decomposition...")
        print(f"Query: {user_query}")
        
        # Step 1: Initial decomposition with o3
        initial_decomposition = await self._initial_decomposition(user_query, debug_mode)
        
        # Step 2: Iterative refinement based on available data
        refined_decomposition = await self._iterative_refinement(initial_decomposition, debug_mode)
        
        # Step 3: Execute the decomposed steps
        executed_decomposition = await self._execute_decomposition(refined_decomposition, debug_mode)
        
        return executed_decomposition

    async def _initial_decomposition(self, user_query: str, debug_mode: bool = False) -> QueryDecomposition:
        """Use o3 to create initial query decomposition"""
        
        available_tools = FinanceToolRegistry.format_tools_for_llm()
        
        system_prompt = f"""You are an expert financial analyst with access to a powerful reasoning system. 
Your task is to decompose complex financial queries into three types of executable steps:

1. **DATA RETRIEVAL** - Use YFinance tools to get raw financial data
2. **ANALYSIS** - Use GPT-4o reasoning to calculate, process, and analyze the data  
3. **OUTPUT** - Format and display the final results nicely

Available YFinance Tools:
{available_tools}

CRITICAL INSTRUCTIONS:
1. Create steps in logical sequence: DATA → ANALYSIS → OUTPUT
2. DATA steps: Use specific YFinance tools to retrieve raw data
3. ANALYSIS steps: Define what calculations/processing needs to be done
4. OUTPUT steps: Define how to present the final results
5. Each step should have proper dependencies (analysis depends on data, output depends on analysis)

For each step, provide:
- step_id: unique identifier (step_1, step_2, etc.)
- description: what this step accomplishes  
- step_type: "DATA", "ANALYSIS", or "OUTPUT"
- depends_on: list of step_ids this step depends on

For DATA steps also provide:
- tool_name: exact name from available YFinance tools
- parameters: specific parameters for the tool

For ANALYSIS steps also provide:
- analysis_prompt: detailed prompt for GPT-4o to process the data

For OUTPUT steps also provide:
- output_template: instructions for formatting the final display

Example format:
{{
  "reasoning": "User wants to compare revenue growth. I need to: 1) Get income data for both companies, 2) Calculate growth rates, 3) Display comparison nicely",
  "steps": [
    {{
      "step_id": "step_1",
      "description": "Get AAPL income statements for last 4 quarters",
      "step_type": "DATA",
      "tool_name": "get_income_statements",
      "parameters": {{"ticker": "AAPL", "period": "quarterly", "limit": 4}},
      "depends_on": []
    }},
    {{
      "step_id": "step_2", 
      "description": "Calculate revenue growth rates for both companies",
      "step_type": "ANALYSIS",
      "analysis_prompt": "Calculate quarter-over-quarter revenue growth rates for both companies and compare them",
      "depends_on": ["step_1"]
    }},
    {{
      "step_id": "step_3",
      "description": "Display revenue growth comparison",
      "step_type": "OUTPUT", 
      "output_template": "Create a clear comparison table showing revenue growth rates",
      "depends_on": ["step_2"]
    }}
  ]
}}"""

        user_prompt = f"""Please decompose this financial query into executable steps:

Query: {user_query}

Think carefully about:
1. What specific financial data is needed?
2. Which companies/tickers are involved?
3. What time periods are relevant?
4. What calculations or comparisons need to be made?
5. In what order should the data be retrieved?

Provide a detailed reasoning and step-by-step decomposition."""

        try:
            if debug_mode:
                print(f"\n🔍 DEBUG: Sending prompt to GPT-4o...")
                print(f"📝 User Prompt: {user_prompt[:200]}...")
                print(f"🛠️  Available Tools: {len(FinanceToolRegistry.TOOLS)} tools")
            
            # Use o3-mini for reasoning (o3 may not be available yet, fallback to best available)
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",  # Using gpt-4o as it's more widely available than o1-preview
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_completion_tokens=4000
            )
            
            # Parse the JSON response
            response_text = response.choices[0].message.content
            
            if debug_mode:
                print(f"\n🤖 GPT-4o Response:")
                print("="*60)
                print(response_text)
                print("="*60)
            
            # Try to extract JSON from the response
            try:
                # Find JSON in the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                json_str = response_text[json_start:json_end]
                
                decomp_data = json.loads(json_str)
                
                # Convert to our data structures
                steps = []
                for step_data in decomp_data.get('steps', []):
                    step = DecompositionStep(
                        step_id=step_data['step_id'],
                        description=step_data['description'],
                        step_type=step_data['step_type'],
                        tool_name=step_data.get('tool_name'),
                        parameters=step_data.get('parameters', {}),
                        analysis_prompt=step_data.get('analysis_prompt'),
                        output_template=step_data.get('output_template'),
                        depends_on=step_data.get('depends_on', [])
                    )
                    steps.append(step)
                
                decomposition = QueryDecomposition(
                    query=user_query,
                    steps=steps,
                    reasoning=decomp_data.get('reasoning', ''),
                    status="in_progress"
                )
                
                if debug_mode:
                    print(f"\n📋 DECOMPOSED QUERY:")
                    print(f"🎯 Original Query: {user_query}")
                    print(f"🧠 AI Reasoning: {decomposition.reasoning}")
                    print(f"📝 Generated {len(steps)} Steps:")
                    for i, step in enumerate(steps, 1):
                        print(f"   {i}. {step.step_id} ({step.step_type}): {step.description}")
                        if step.step_type == "DATA":
                            print(f"      Tool: {step.tool_name}")
                            print(f"      Parameters: {step.parameters}")
                        elif step.step_type == "ANALYSIS":
                            print(f"      Analysis Prompt: {step.analysis_prompt[:100]}...")
                        elif step.step_type == "OUTPUT":
                            print(f"      Output Template: {step.output_template}")
                        if step.depends_on:
                            print(f"      Depends on: {step.depends_on}")
                        print()
                
                return decomposition
                
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON from o3 response: {e}")
                print(f"Response text: {response_text}")
                raise ValueError(f"Invalid JSON response from o3: {e}")
                
        except Exception as e:
            print(f"❌ Error in initial decomposition: {e}")
            raise

    async def _iterative_refinement(self, decomposition: QueryDecomposition, debug_mode: bool = False) -> QueryDecomposition:
        """
        Iteratively refine the decomposition based on available data and results
        This is where the magic happens - o3 can see partial results and adjust the plan
        """
        print(f"\n🔄 Iterative Refinement: Checking data availability...")
        
        # For now, we'll keep the initial decomposition
        # In a more advanced version, this would:
        # 1. Test if tools/tickers are available
        # 2. Adjust parameters based on data availability
        # 3. Add or remove steps based on findings
        # 4. Reorder steps for optimal execution
        
        # Validate steps based on their types
        available_tools = await self.finance_client.get_available_tools()
        
        if debug_mode:
            print(f"\n🔧 REFINEMENT PHASE:")
            print(f"🛠️  Available YFinance Tools: {available_tools}")
            print(f"🔍 Validating {len(decomposition.steps)} steps...")
        
        for step in decomposition.steps:
            if step.step_type == "DATA":
                # Validate DATA steps have valid YFinance tools
                if not step.tool_name:
                    step.status = "failed"
                    step.error = "DATA step missing tool_name"
                elif step.tool_name not in available_tools:
                    step.status = "failed"
                    step.error = f"Tool '{step.tool_name}' not available"
                elif debug_mode:
                    print(f"✅ Step {step.step_id} (DATA): Tool {step.tool_name} is available")
                    
            elif step.step_type == "ANALYSIS":
                # Validate ANALYSIS steps have analysis prompt
                if not step.analysis_prompt:
                    step.status = "failed"
                    step.error = "ANALYSIS step missing analysis_prompt"
                elif debug_mode:
                    print(f"✅ Step {step.step_id} (ANALYSIS): Has analysis prompt")
                    
            elif step.step_type == "OUTPUT":
                # Validate OUTPUT steps have output template
                if not step.output_template:
                    step.status = "failed"
                    step.error = "OUTPUT step missing output_template"
                elif debug_mode:
                    print(f"✅ Step {step.step_id} (OUTPUT): Has output template")
                    
            else:
                step.status = "failed"
                step.error = f"Unknown step type: {step.step_type}"
                
            if step.status == "failed" and not debug_mode:
                print(f"⚠️  Step {step.step_id}: {step.error}")
        
        print(f"✅ Refinement complete. {len(decomposition.steps)} steps ready for execution.")
        return decomposition

    async def _execute_decomposition(self, decomposition: QueryDecomposition, debug_mode: bool = False) -> QueryDecomposition:
        """Execute the decomposed steps in the correct order based on step type"""
        print(f"\n🚀 Executing decomposition steps...")
        
        executed_steps = {}
        
        # Execute steps respecting dependencies
        for step in decomposition.steps:
            if step.status == "failed":
                continue
                
            # Check if dependencies are satisfied
            dependencies_ready = all(
                dep_id in executed_steps and executed_steps[dep_id].status == "completed"
                for dep_id in step.depends_on
            )
            
            if not dependencies_ready:
                step.status = "failed"
                step.error = "Dependencies not satisfied"
                continue
            
            # Execute the step based on its type
            step.status = "in_progress"
            print(f"🔧 Executing {step.step_id} ({step.step_type}): {step.description}")
            
            try:
                if step.step_type == "DATA":
                    await self._execute_data_step(step, debug_mode)
                elif step.step_type == "ANALYSIS":
                    await self._execute_analysis_step(step, executed_steps, debug_mode)
                elif step.step_type == "OUTPUT":
                    await self._execute_output_step(step, executed_steps, debug_mode)
                else:
                    step.status = "failed"
                    step.error = f"Unknown step type: {step.step_type}"
                    
            except Exception as e:
                step.status = "failed"
                step.error = str(e)
                print(f"❌ {step.step_id} failed with exception: {e}")
                if debug_mode:
                    import traceback
                    print(f"   🐛 Full traceback:")
                    traceback.print_exc()
            
            executed_steps[step.step_id] = step
        
        # Generate final summary
        decomposition.final_analysis = await self._generate_final_analysis(decomposition)
        
        # Determine overall status
        failed_steps = [s for s in decomposition.steps if s.status == "failed"]
        if failed_steps:
            decomposition.status = "partially_completed"
            print(f"⚠️  Decomposition completed with {len(failed_steps)} failed steps")
        else:
            decomposition.status = "completed"
            print(f"🎉 All steps completed successfully!")
        
        return decomposition

    async def _execute_data_step(self, step: DecompositionStep, debug_mode: bool = False):
        """Execute a DATA step using YFinance client"""
        if debug_mode:
            print(f"   📞 Calling YFinance Tool: {step.tool_name}")
            print(f"   📋 Parameters: {step.parameters}")
        
        result = await self.finance_client.execute_mcp_call(
            step.tool_name, 
            **step.parameters
        )
        
        if debug_mode:
            print(f"   📨 YFinance Response:")
            print(f"      Success: {result.success}")
            if result.success:
                print(f"      Data Type: {type(result.data)}")
                if isinstance(result.data, dict):
                    print(f"      Data Keys: {list(result.data.keys())}")
                    # Show first few items of data for debugging
                    for key, value in list(result.data.items())[:3]:
                        if isinstance(value, (str, int, float)):
                            print(f"      {key}: {value}")
                        elif isinstance(value, dict):
                            print(f"      {key}: dict with {len(value)} items")
                        elif isinstance(value, list):
                            print(f"      {key}: list with {len(value)} items")
                        else:
                            print(f"      {key}: {type(value)}")
            else:
                print(f"      Error: {result.error}")
        
        if result.success:
            step.status = "completed"
            step.result = result.data
            print(f"✅ {step.step_id} completed successfully")
        else:
            step.status = "failed"
            step.error = result.error
            print(f"❌ {step.step_id} failed: {result.error}")

    async def _execute_analysis_step(self, step: DecompositionStep, executed_steps: Dict, debug_mode: bool = False):
        """Execute an ANALYSIS step using GPT-4o reasoning"""
        if debug_mode:
            print(f"   🧠 Running GPT-4o Analysis")
            print(f"   📝 Analysis Prompt: {step.analysis_prompt}")
        
        # Gather data from dependency steps
        dependency_data = {}
        for dep_id in step.depends_on:
            if dep_id in executed_steps and executed_steps[dep_id].status == "completed":
                dependency_data[dep_id] = executed_steps[dep_id].result
        
        # Clean the data to make it JSON serializable
        cleaned_dependency_data = self._clean_data_for_json(dependency_data)
        
        analysis_prompt = f"""
        {step.analysis_prompt}
        
        Available Data from Previous Steps:
        {json.dumps(cleaned_dependency_data, indent=2, default=str)}
        
        Please provide a detailed analysis based on this data. Be specific with calculations and insights.
        """
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.1,
            max_completion_tokens=2000
        )
        
        analysis_result = response.choices[0].message.content
        
        step.status = "completed"
        step.result = analysis_result
        print(f"✅ {step.step_id} completed successfully")
        
        if debug_mode:
            print(f"   📊 Analysis Result: {analysis_result[:200]}...")

    def _clean_data_for_json(self, data):
        """Clean data to make it JSON serializable by converting timestamp keys to strings"""
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                # Convert timestamp keys to strings
                if hasattr(key, 'strftime'):  # pandas Timestamp
                    str_key = key.strftime('%Y-%m-%d') if hasattr(key, 'strftime') else str(key)
                else:
                    str_key = str(key)
                cleaned[str_key] = self._clean_data_for_json(value)
            return cleaned
        elif isinstance(data, list):
            return [self._clean_data_for_json(item) for item in data]
        else:
            return data

    async def _execute_output_step(self, step: DecompositionStep, executed_steps: Dict, debug_mode: bool = False):
        """Execute an OUTPUT step to format and display results"""
        if debug_mode:
            print(f"   🎨 Formatting Output")
            print(f"   📋 Output Template: {step.output_template}")
        
        # Import the LLM output formatter
        from .llm_output_formatter import LLMOutputFormatter
        formatter = LLMOutputFormatter(self.openai_api_key)
        
        # Gather all previous results
        all_data = {}
        for dep_id in step.depends_on:
            if dep_id in executed_steps and executed_steps[dep_id].status == "completed":
                all_data[dep_id] = executed_steps[dep_id].result
        
        # Clean the data to make it JSON serializable
        cleaned_data = self._clean_data_for_json(all_data)
        
        output_prompt = f"""
        Create a comprehensive financial analysis report based on the following instructions: {step.output_template}
        
        Available Data:
        {json.dumps(cleaned_data, indent=2, default=str)}
        
        IMPORTANT: Structure your response to include:
        1. A clear summary of key findings
        2. Specific metrics and numbers with context
        3. Tables for comparative data when appropriate  
        4. Key insights and implications
        5. Clear conclusions
        
        Format the response in a clear, professional manner suitable for financial reporting.
        Include specific numbers, percentages, and comparisons where relevant.
        """
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": output_prompt}
            ],
            temperature=0.1,
            max_completion_tokens=2000
        )
        
        formatted_output = response.choices[0].message.content
        
        # Create structured output for frontend using LLM
        structured_result = await formatter.format_for_frontend(
            formatted_output, 
            cleaned_data, 
            self.current_query  # Pass the original query for context
        )
        
        step.status = "completed"
        step.result = {
            "raw_output": formatted_output,
            "structured_output": structured_result
        }
        print(f"✅ {step.step_id} completed successfully")
        
        # Display the formatted output
        print(f"\n🎯 {step.description}:")
        print("-" * 50)
        print(formatted_output)

    async def _generate_final_analysis(self, decomposition: QueryDecomposition) -> str:
        """Generate a simple summary since OUTPUT steps handle the detailed formatting"""
        
        completed_steps = [s for s in decomposition.steps if s.status == "completed"]
        failed_steps = [s for s in decomposition.steps if s.status == "failed"]
        
        summary = f"Query processing completed:\n"
        summary += f"✅ {len(completed_steps)} steps completed successfully\n"
        
        if failed_steps:
            summary += f"❌ {len(failed_steps)} steps failed\n"
            
        # The detailed analysis and output is now handled by the OUTPUT steps
        summary += "\nDetailed results have been displayed above by the OUTPUT steps."
        
        return summary


# Helper functions for common query patterns
class QueryPatterns:
    """Common financial query patterns for better decomposition"""
    
    @staticmethod
    def detect_query_type(query: str) -> str:
        """Detect the type of financial query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['compare', 'comparison', 'vs', 'versus']):
            return "comparison"
        elif any(word in query_lower for word in ['trend', 'over time', 'historical', 'growth']):
            return "trend_analysis"
        elif any(word in query_lower for word in ['current', 'latest', 'today', 'now']):
            return "current_data"
        elif any(word in query_lower for word in ['news', 'announcement', 'events']):
            return "news_analysis"
        elif any(word in query_lower for word in ['financial', 'statements', 'income', 'balance', 'cash flow']):
            return "financial_statements"
        else:
            return "general"
    
    @staticmethod
    def extract_tickers(query: str) -> List[str]:
        """Extract likely ticker symbols from query"""
        import re
        
        # Look for patterns like AAPL, MSFT, TSLA (2-5 uppercase letters)
        ticker_pattern = r'\b[A-Z]{2,5}\b'
        potential_tickers = re.findall(ticker_pattern, query)
        
        # Filter out common false positives
        false_positives = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'HAD', 'DAY', 'GET', 'USE', 'MAN', 'NEW', 'NOW', 'WAY', 'MAY', 'SAY', 'SEE', 'HIM', 'TWO', 'HOW', 'ITS', 'WHO', 'OIL', 'DID', 'YES', 'HIS', 'HAS', 'HAD', 'LET', 'PUT', 'TOO', 'OLD', 'WHY', 'ANY', 'AGO', 'OFF', 'FAR', 'SET', 'OWN', 'END'}
        
        # Also look for common company names and map to tickers
        company_ticker_map = {
            'apple': 'AAPL',
            'microsoft': 'MSFT', 
            'google': 'GOOGL',
            'alphabet': 'GOOGL',
            'amazon': 'AMZN',
            'tesla': 'TSLA',
            'nvidia': 'NVDA',
            'meta': 'META',
            'facebook': 'META',
            'netflix': 'NFLX',
            'disney': 'DIS',
            'intel': 'INTC',
            'amd': 'AMD',
            'oracle': 'ORCL',
            'salesforce': 'CRM',
            'adobe': 'ADBE'
        }
        
        query_lower = query.lower()
        found_tickers = []
        
        # Add explicit ticker symbols
        found_tickers.extend([ticker for ticker in potential_tickers if ticker not in false_positives])
        
        # Add company name mappings
        for company, ticker in company_ticker_map.items():
            if company in query_lower:
                found_tickers.append(ticker)
        
        # Remove duplicates and return
        return list(set(found_tickers)) 