#!/usr/bin/env python3
"""
LLM-Based Output Formatter for Sankhya Finance
Uses GPT-4o to intelligently convert analysis results into structured JSON for beautiful frontend display
"""

import json
import openai
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio

class LLMOutputFormatter:
    """LLM-powered formatter that creates intelligent structured output for frontend consumption"""
    
    def __init__(self, openai_api_key: str):
        self.openai_client = openai.AsyncOpenAI(api_key=openai_api_key)
    
    async def format_for_frontend(self, 
                                raw_output: str, 
                                step_data: Dict[str, Any], 
                                original_query: str) -> Dict[str, Any]:
        """
        Use GPT-4o to intelligently convert raw analysis + data into both structured JSON 
        and executable TypeScript/React components for frontend
        """
        
        # Generate both structured JSON and TypeScript components
        structured_json = await self._generate_structured_json(raw_output, step_data, original_query)
        typescript_component = await self._generate_typescript_component(raw_output, step_data, original_query)
        
        # Combine both outputs
        result = structured_json.copy()
        result["typescript_component"] = typescript_component
        result["rendering_mode"] = "hybrid"  # Both JSON and TypeScript available
        
        return result
    
    async def _generate_structured_json(self, 
                                      raw_output: str, 
                                      step_data: Dict[str, Any], 
                                      original_query: str) -> Dict[str, Any]:
        """
        Use GPT-4o to intelligently convert raw analysis + data into structured JSON for frontend
        
        Returns structured JSON with content blocks that frontend can render beautifully
        """
        
                 # Prepare the data context for the LLM
        data_context = self._prepare_data_context(step_data)
        
        # Create the JSON formatting prompt
        formatting_prompt = f"""
You are an expert financial data visualization specialist. Your task is to convert raw financial analysis results into a perfectly structured JSON format that a frontend can use to create beautiful, interactive displays.

ORIGINAL USER QUERY: "{original_query}"

RAW ANALYSIS OUTPUT:
{raw_output}

UNDERLYING DATA:
{json.dumps(data_context, indent=2, default=str)}

Your task is to create a JSON response with the following EXACT structure:

{{
  "summary": "A clear, concise 1-2 sentence summary of the key findings",
  "content_blocks": [
    {{
      "type": "metric",
      "title": "Descriptive Title",
      "data": {{
        "value": "Formatted value (e.g., $156.23, 15.4%, 2.3x)",
        "label": "What this metric represents",
        "trend": "up/down/neutral (if applicable)",
        "context": "Brief context about this metric"
      }}
    }},
    {{
      "type": "table",
      "title": "Descriptive Title",
      "data": {{
        "headers": ["Column 1", "Column 2", "Column 3"],
        "rows": [
          ["Row 1 Data", "Row 1 Data", "Row 1 Data"],
          ["Row 2 Data", "Row 2 Data", "Row 2 Data"]
        ],
        "highlight_column": 2,
        "sort_by": "Column 2"
      }}
    }},
    {{
      "type": "chart",
      "title": "Descriptive Title", 
      "data": {{
        "chart_type": "line/bar/pie/area",
        "x_axis_label": "X Axis Label",
        "y_axis_label": "Y Axis Label",
        "datasets": [
          {{
            "name": "Dataset Name",
            "color": "#3498db",
            "data": [
              {{"x": "Label", "y": 123.45}},
              {{"x": "Label", "y": 234.56}}
            ]
          }}
        ]
      }}
    }},
    {{
      "type": "comparison",
      "title": "Company/Metric Comparison",
      "data": {{
        "items": [
          {{
            "name": "Item 1",
            "value": "Value 1",
            "trend": "up/down/neutral",
            "percentage": "+5.2%"
          }},
          {{
            "name": "Item 2", 
            "value": "Value 2",
            "trend": "down",
            "percentage": "-2.1%"
          }}
        ]
      }}
    }},
    {{
      "type": "insight",
      "title": "Key Insight",
      "data": {{
        "content": "Important insight derived from the analysis",
        "importance": "high/medium/low",
        "category": "performance/risk/opportunity/trend"
      }}
    }}
  ],
  "key_insights": [
    "Most important insight from the analysis",
    "Second most important insight",
    "Third insight (if applicable)"
  ],
  "recommendations": [
    "Actionable recommendation based on analysis",
    "Additional recommendation if applicable"  
  ],
  "metadata": {{
    "query_type": "stock_price/comparison/trend_analysis/financial_metrics",
    "companies_analyzed": ["AAPL", "MSFT"],
    "time_period": "Current/Q4 2024/Last 5 years",
    "confidence": "high/medium/low"
  }}
}}

CRITICAL FORMATTING RULES:
1. Extract ONLY the most relevant and important information for the user's specific query
2. Choose content block types that best represent the data (metrics for key numbers, tables for comparisons, charts for trends)
3. Format all financial values appropriately (currency, percentages, ratios)
4. Make titles descriptive and specific to the query context
5. Include trends and context where relevant
6. Prioritize content blocks by importance to the query
7. If there's time series data, create chart blocks
8. If there's comparative data, create comparison or table blocks
9. Always include 2-4 key insights that directly answer the user's question
10. Return ONLY valid JSON, no additional text

Based on the user's query "{original_query}", intelligently select and structure the most relevant content blocks that directly address what they asked for.
"""

        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a financial data visualization expert. You convert raw financial analysis into perfectly structured JSON for frontend display. Always return valid JSON only."},
                    {"role": "user", "content": formatting_prompt}
                ],
                temperature=0.1,
                max_completion_tokens=3000
            )
            
            formatted_json_str = response.choices[0].message.content.strip()
            
            # Parse and validate the JSON
            try:
                structured_output = json.loads(formatted_json_str)
                
                # Add timestamp and completion status
                structured_output["timestamp"] = datetime.now().isoformat()
                structured_output["query_completed"] = True
                structured_output["formatting_version"] = "llm_v1"
                
                return structured_output
                
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON from LLM formatter: {e}")
                print(f"Raw response: {formatted_json_str[:500]}...")
                
                # Fallback to basic structure
                return self._create_fallback_structure(raw_output, original_query)
                
        except Exception as e:
            print(f"❌ Error in LLM formatting: {e}")
            return self._create_fallback_structure(raw_output, original_query)
    
    async def _generate_typescript_component(self, 
                                           raw_output: str, 
                                           step_data: Dict[str, Any], 
                                           original_query: str) -> Dict[str, Any]:
        """Generate TypeScript/React component code for rendering the analysis"""
        
        data_context = self._prepare_data_context(step_data)
        
        typescript_prompt = f"""
You are an expert React/TypeScript developer specializing in financial data visualization. 
Create a beautiful, interactive React component that renders the financial analysis results.

ORIGINAL USER QUERY: "{original_query}"

RAW ANALYSIS OUTPUT:
{raw_output}

UNDERLYING DATA:
{json.dumps(data_context, indent=2, default=str)}

Generate a complete TypeScript React component with the following specifications:

1. **Component Structure**: Create a functional component called `FinancialAnalysisDisplay`
2. **Styling**: Use Tailwind CSS for styling (assume it's available)
3. **Interactivity**: Make it interactive where appropriate (hover effects, expandable sections)
4. **Data Visualization**: Choose appropriate visualization methods:
   - Key metrics → Large number cards with trend indicators
   - Tables → Responsive, sortable tables
   - Time series → Line charts using Recharts library
   - Comparisons → Side-by-side comparison cards
   - Insights → Highlighted callout boxes

5. **Icons**: Use Lucide React icons (assume available: TrendingUp, TrendingDown, DollarSign, BarChart3, Info, etc.)

6. **Responsive Design**: Mobile-friendly layout

7. **TypeScript**: Proper typing for all props and data

Return ONLY a JSON object with this structure:
{{
  "component_code": "// Complete TypeScript React component code here",
  "required_dependencies": ["recharts", "lucide-react", "tailwindcss"],
  "component_name": "FinancialAnalysisDisplay",
  "props_interface": "interface Props {{ ... }}",
  "usage_example": "// How to use this component"
}}

CRITICAL REQUIREMENTS:
- The component must be self-contained and executable
- Include proper TypeScript interfaces
- Use modern React functional component syntax
- Make it visually appealing and professional
- Ensure all data from the analysis is properly displayed
- Add loading states and error handling where appropriate
- Include proper accessibility attributes

Generate a component that directly addresses the user's query: "{original_query}"

Focus on creating the most appropriate visualization for this specific financial query.
"""

        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a React/TypeScript expert who creates beautiful financial data visualizations. Always return valid JSON with component code."},
                    {"role": "user", "content": typescript_prompt}
                ],
                temperature=0.1,
                max_completion_tokens=4000
            )
            
            typescript_response = response.choices[0].message.content.strip()
            
            try:
                typescript_data = json.loads(typescript_response)
                
                # Add metadata
                typescript_data["generated_at"] = datetime.now().isoformat()
                typescript_data["query_context"] = original_query
                typescript_data["framework"] = "React/TypeScript"
                
                return typescript_data
                
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON from TypeScript generator: {e}")
                print(f"Raw response: {typescript_response[:500]}...")
                
                return self._create_fallback_typescript()
                
        except Exception as e:
            print(f"❌ Error generating TypeScript component: {e}")
            return self._create_fallback_typescript()
    
    def _create_fallback_typescript(self) -> Dict[str, Any]:
        """Create a basic fallback TypeScript component"""
        
        fallback_component = '''
import React from 'react';
import { AlertCircle } from 'lucide-react';

interface Props {
  data?: any;
  error?: string;
}

const FinancialAnalysisDisplay: React.FC<Props> = ({ data, error }) => {
  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
        <div className="flex items-center space-x-2">
          <AlertCircle className="h-5 w-5 text-red-500" />
          <span className="text-red-700">Error loading analysis: {error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 bg-white border border-gray-200 rounded-lg shadow">
      <h2 className="text-xl font-bold text-gray-900 mb-4">Financial Analysis</h2>
      <div className="text-gray-600">
        <p>Analysis completed successfully.</p>
        <p className="mt-2 text-sm">
          Note: Fallback component used. Please check the raw analysis data.
        </p>
      </div>
    </div>
  );
};

export default FinancialAnalysisDisplay;
'''
        
        return {
            "component_code": fallback_component.strip(),
            "required_dependencies": ["react", "lucide-react", "tailwindcss"],
            "component_name": "FinancialAnalysisDisplay",
            "props_interface": "interface Props { data?: any; error?: string; }",
            "usage_example": "<FinancialAnalysisDisplay data={analysisData} />",
            "generated_at": datetime.now().isoformat(),
            "query_context": "fallback",
            "framework": "React/TypeScript",
            "note": "Fallback component due to generation error"
        }
    
    def _prepare_data_context(self, step_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the raw step data for LLM consumption"""
        cleaned_data = {}
        
        for step_id, step_result in step_data.items():
            if step_result is not None:
                # Clean and simplify the data
                if isinstance(step_result, dict):
                    # Remove None values and simplify complex nested structures
                    cleaned_step = {}
                    for key, value in step_result.items():
                        if value is not None:
                            if isinstance(value, (dict, list)) and len(str(value)) > 1000:
                                # Truncate very large nested structures
                                cleaned_step[key] = f"<Large data structure with {len(value) if isinstance(value, (list, dict)) else 'complex'} items>"
                            else:
                                cleaned_step[key] = value
                    cleaned_data[step_id] = cleaned_step
                else:
                    # For non-dict results, include directly
                    result_str = str(step_result)
                    if len(result_str) > 500:
                        cleaned_data[step_id] = result_str[:500] + "..."
                    else:
                        cleaned_data[step_id] = step_result
        
        return cleaned_data
    
    def _create_fallback_structure(self, raw_output: str, original_query: str) -> Dict[str, Any]:
        """Create a basic fallback structure if LLM formatting fails"""
        
        return {
            "summary": f"Analysis completed for: {original_query}",
            "content_blocks": [
                {
                    "type": "text",
                    "title": "Analysis Results",
                    "data": {
                        "content": raw_output[:1000] + "..." if len(raw_output) > 1000 else raw_output
                    }
                }
            ],
            "key_insights": [
                "Analysis completed successfully",
                "Raw results available in text format"
            ],
            "recommendations": [],
            "metadata": {
                "query_type": "general",
                "confidence": "medium",
                "note": "Fallback formatting used due to processing error"
            },
            "timestamp": datetime.now().isoformat(),
            "query_completed": True,
            "formatting_version": "fallback_v1"
        }

class StreamingLLMFormatter:
    """Formatter for streaming responses with LLM enhancement"""
    
    def __init__(self, openai_api_key: str):
        self.formatter = LLMOutputFormatter(openai_api_key)
    
    async def format_streaming_output(self, 
                                    raw_output: str, 
                                    step_data: Dict[str, Any], 
                                    original_query: str) -> Dict[str, Any]:
        """Format output for streaming response with LLM enhancement"""
        
        structured_output = await self.formatter.format_for_frontend(
            raw_output, step_data, original_query
        )
        
        return {
            "type": "final_structured_output",
            "data": {
                "message": "🎨 AI-Enhanced Analysis Complete - Beautiful Results Ready",
                "structured_output": structured_output,
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def format_step_preview(self, step_id: str, step_result: Any, step_description: str) -> Dict[str, Any]:
        """Format individual step output preview for streaming"""
        
        # Create a quick preview without full LLM processing
        preview_text = ""
        if isinstance(step_result, dict):
            # Show key metrics from dict results
            key_items = []
            for key, value in list(step_result.items())[:3]:  # First 3 items
                if value is not None:
                    if isinstance(value, (int, float)):
                        if key.lower() in ['currentprice', 'price']:
                            key_items.append(f"{key}: ${value:.2f}")
                        elif key.lower() in ['marketcap']:
                            if value > 1e9:
                                key_items.append(f"{key}: ${value/1e9:.1f}B")
                            else:
                                key_items.append(f"{key}: ${value/1e6:.1f}M")
                        else:
                            key_items.append(f"{key}: {value}")
                    else:
                        str_value = str(value)
                        if len(str_value) > 50:
                            str_value = str_value[:50] + "..."
                        key_items.append(f"{key}: {str_value}")
            
            preview_text = " | ".join(key_items) if key_items else "Data retrieved successfully"
        else:
            result_str = str(step_result)
            preview_text = result_str[:100] + "..." if len(result_str) > 100 else result_str
        
        return {
            "type": "step_result_preview",
            "data": {
                "step_id": step_id,
                "description": step_description,
                "preview": preview_text,
                "timestamp": datetime.now().isoformat()
            }
        } 