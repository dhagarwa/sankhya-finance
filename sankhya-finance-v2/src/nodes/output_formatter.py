"""
OutputFormatter Node - The final node before END.

This node takes all the accumulated step results and produces two outputs:

1. **Structured JSON** - A frontend-friendly JSON structure with content blocks
   (metrics, tables, charts, comparisons, insights) that a React app can render.

2. **TypeScript Component** - A complete React/TypeScript component that renders
   the analysis results using Tailwind CSS and Recharts.

This replaces v1's LLMOutputFormatter class. The key improvement is that
this is a single node call instead of a separate class with its own model
config, client management, and error handling.

Flow:
    Verifier (all_done) -> [this node] -> END
    DirectResponse       -> [this node] -> END
"""

import json
from datetime import datetime
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.state import FinanceState, StepResult, StepType
from src.utils.model_config import get_llm


# =============================================================================
# Structured JSON Prompt
# =============================================================================

STRUCTURED_JSON_PROMPT = """You are an expert financial data visualization specialist.

Convert the analysis results into a structured JSON format for frontend display.

ORIGINAL USER QUERY: "{query}"

ANALYSIS RESULTS:
{raw_analysis}

UNDERLYING DATA:
{data_summary}

Create a JSON response with this EXACT structure:
{{
  "summary": "Clear 1-2 sentence summary of key findings",
  "content_blocks": [
    {{
      "type": "metric",
      "title": "Descriptive Title",
      "data": {{
        "value": "Formatted value (e.g., $156.23, 15.4%, 2.3x)",
        "label": "What this metric represents",
        "trend": "up/down/neutral",
        "context": "Brief context"
      }}
    }},
    {{
      "type": "table",
      "title": "Table Title",
      "data": {{
        "headers": ["Col1", "Col2", "Col3"],
        "rows": [["data", "data", "data"]]
      }}
    }},
    {{
      "type": "chart",
      "title": "Chart Title",
      "data": {{
        "chart_type": "line/bar/pie",
        "x_axis_label": "X Label",
        "y_axis_label": "Y Label",
        "datasets": [
          {{"name": "Dataset", "data": [{{"x": "Label", "y": 123.45}}]}}
        ]
      }}
    }},
    {{
      "type": "insight",
      "title": "Key Insight",
      "data": {{
        "content": "Important insight from the analysis",
        "importance": "high/medium/low"
      }}
    }}
  ],
  "key_insights": ["Insight 1", "Insight 2", "Insight 3"],
  "recommendations": ["Recommendation 1"],
  "metadata": {{
    "query_type": "stock_price/comparison/trend_analysis/financial_metrics",
    "companies_analyzed": ["AAPL"],
    "confidence": "high/medium/low"
  }}
}}

Rules:
1. Choose content block types that best represent the data
2. Format financial values with proper currency/percentage notation
3. Include 2-4 key insights that directly answer the user's question
4. Prioritize content blocks by importance
5. Return ONLY valid JSON"""


# =============================================================================
# TypeScript Component Prompt
# =============================================================================

TYPESCRIPT_PROMPT = """You are an expert React/TypeScript developer specializing in financial data visualization.

Create a React component that renders these financial analysis results.

QUERY: "{query}"
ANALYSIS: {raw_analysis}
DATA: {data_summary}

Requirements:
1. Functional component named `FinancialAnalysisDisplay`
2. Use Tailwind CSS for styling
3. Use Recharts for any charts (LineChart, BarChart, etc.)
4. Use Lucide React icons (TrendingUp, TrendingDown, DollarSign, BarChart3, etc.)
5. Include TypeScript interfaces for all data
6. Mobile-responsive layout
7. Professional, clean design

Return ONLY a JSON object:
{{
  "component_code": "// Complete TypeScript React component",
  "component_name": "FinancialAnalysisDisplay",
  "required_dependencies": ["recharts", "lucide-react"],
  "props_interface": "interface Props {{ ... }}"
}}

Return ONLY valid JSON."""


# =============================================================================
# Node Function
# =============================================================================


async def output_formatter(state: FinanceState) -> dict[str, Any]:
    """
    Format all results into structured JSON and a TypeScript component.

    This node:
        1. Combines all step results into a raw analysis summary
        2. Calls the LLM to produce structured JSON for frontend display
        3. Calls the LLM to produce a TypeScript React component
        4. Stores both in state for the final output

    Args:
        state: The current FinanceState.

    Returns:
        Partial state update with structured_output and typescript_component.
    """
    query = state.get("query", "")
    step_results = state.get("step_results", {})

    # --- Build raw analysis from all step results ---
    raw_analysis = state.get("raw_analysis", "")

    if not raw_analysis:
        # If no raw_analysis yet (financial query path), build from step results
        raw_analysis = _build_raw_analysis(step_results)

    # --- Build data summary for the LLM ---
    data_summary = _build_data_summary(step_results)

    # --- Generate structured JSON and TypeScript in parallel ---
    # (We could use asyncio.gather here, but sequential is simpler and
    #  the LLM calls are the bottleneck anyway)

    structured_output = await _generate_structured_json(query, raw_analysis, data_summary)
    typescript_component = await _generate_typescript(query, raw_analysis, data_summary)

    return {
        "raw_analysis": raw_analysis,
        "structured_output": structured_output,
        "typescript_component": typescript_component,
        "messages": state.get("messages", []) + [
            f"[OutputFormatter] Generated structured output "
            f"({len(structured_output.get('content_blocks', []))} content blocks) "
            f"and TypeScript component"
        ],
        "total_node_calls": state.get("total_node_calls", 0) + 1,
    }


# =============================================================================
# Internal Functions
# =============================================================================


def _build_raw_analysis(step_results: dict[str, Any]) -> str:
    """
    Combine all step results into a single text summary.

    Uses typed StepResult models to access data cleanly:
        - DATA results: serialize the .data dict
        - ANALYSIS results: include the .analysis text directly
        - Failed results: note the error
    """
    parts = []

    for step_id, result in step_results.items():
        if isinstance(result, StepResult):
            # Typed StepResult -- use the proper accessors
            if result.error and not result.success:
                parts.append(f"--- {step_id} ({result.step_type.value}) ---\nError: {result.error}")
            elif result.step_type == StepType.ANALYSIS and result.analysis:
                parts.append(f"--- {step_id} (ANALYSIS) ---\n{result.analysis}")
            elif result.step_type == StepType.DATA and result.data:
                data_str = json.dumps(result.data, indent=2, default=str)
                if len(data_str) > 2000:
                    data_str = data_str[:2000] + "\n... (truncated)"
                parts.append(f"--- {step_id} (DATA) ---\n{data_str}")
            else:
                parts.append(f"--- {step_id} ---\n{result.get_data_for_prompt()}")
        elif isinstance(result, str):
            # Fallback for plain strings
            parts.append(f"--- {step_id} ---\n{result}")
        elif isinstance(result, dict):
            # Fallback for plain dicts
            result_str = json.dumps(result, indent=2, default=str)
            if len(result_str) > 2000:
                result_str = result_str[:2000] + "\n... (truncated)"
            parts.append(f"--- {step_id} ---\n{result_str}")

    return "\n\n".join(parts) if parts else "No analysis results available."


def _build_data_summary(step_results: dict[str, Any]) -> str:
    """
    Build a concise data summary for the LLM prompts.

    Uses typed StepResult models to extract just the relevant data,
    truncating large results to stay within context limits.
    """
    summary_parts: dict[str, Any] = {}
    total_size = 0
    max_size = 6000  # Conservative limit for LLM context

    for step_id, result in step_results.items():
        if result is None:
            continue

        # Extract the actual data from typed StepResult
        if isinstance(result, StepResult):
            if result.data is not None:
                serializable = result.data
            elif result.analysis is not None:
                serializable = result.analysis
            elif result.error:
                serializable = {"error": result.error}
            else:
                continue
        else:
            serializable = result

        result_str = json.dumps(serializable, default=str)

        if total_size + len(result_str) > max_size:
            summary_parts[step_id] = f"<data truncated, original size: {len(result_str)} chars>"
        else:
            summary_parts[step_id] = serializable
            total_size += len(result_str)

    try:
        return json.dumps(summary_parts, indent=2, default=str)
    except (TypeError, ValueError):
        return str(summary_parts)


async def _generate_structured_json(
    query: str,
    raw_analysis: str,
    data_summary: str,
) -> dict[str, Any]:
    """
    Use the LLM to convert raw analysis into structured JSON for frontend.
    """
    prompt = STRUCTURED_JSON_PROMPT.format(
        query=query,
        raw_analysis=raw_analysis[:3000],  # Truncate for context
        data_summary=data_summary[:3000],
    )

    llm = get_llm(temperature=0.1)

    try:
        response = await llm.ainvoke([
            SystemMessage(content="You are a financial data visualization expert. Return only valid JSON."),
            HumanMessage(content=prompt),
        ])

        content = response.content.strip()

        # Clean markdown code blocks
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        structured = json.loads(content.strip())

        # Add metadata
        structured["timestamp"] = datetime.now().isoformat()
        structured["formatting_version"] = "langgraph_v2"

        return structured

    except (json.JSONDecodeError, Exception) as e:
        # Fallback structure if LLM formatting fails
        return _create_fallback_structure(query, raw_analysis, str(e))


async def _generate_typescript(
    query: str,
    raw_analysis: str,
    data_summary: str,
) -> dict[str, Any]:
    """
    Use the LLM to generate a TypeScript React component for the analysis.
    """
    prompt = TYPESCRIPT_PROMPT.format(
        query=query,
        raw_analysis=raw_analysis[:2000],
        data_summary=data_summary[:2000],
    )

    llm = get_llm(temperature=0.1)

    try:
        response = await llm.ainvoke([
            SystemMessage(content="You are a React/TypeScript expert. Return only valid JSON with component code."),
            HumanMessage(content=prompt),
        ])

        content = response.content.strip()

        # Clean markdown
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        ts_data = json.loads(content.strip())

        # Add metadata
        ts_data["generated_at"] = datetime.now().isoformat()
        ts_data["framework"] = "React/TypeScript"

        return ts_data

    except (json.JSONDecodeError, Exception) as e:
        return _create_fallback_typescript(str(e))


def _create_fallback_structure(
    query: str,
    raw_analysis: str,
    error: str,
) -> dict[str, Any]:
    """Fallback JSON structure when LLM formatting fails."""
    return {
        "summary": f"Analysis completed for: {query}",
        "content_blocks": [
            {
                "type": "text",
                "title": "Analysis Results",
                "data": {
                    "content": raw_analysis[:1000] if raw_analysis else "No results available"
                },
            }
        ],
        "key_insights": ["Analysis completed successfully"],
        "recommendations": [],
        "metadata": {
            "query_type": "general",
            "confidence": "medium",
            "note": f"Fallback formatting used: {error}",
        },
        "timestamp": datetime.now().isoformat(),
        "formatting_version": "fallback_v2",
    }


def _create_fallback_typescript(error: str) -> dict[str, Any]:
    """Fallback TypeScript component when generation fails."""
    return {
        "component_code": (
            "import React from 'react';\n"
            "import { AlertCircle } from 'lucide-react';\n\n"
            "const FinancialAnalysisDisplay: React.FC<{data?: any}> = ({ data }) => (\n"
            "  <div className='p-6 bg-white border rounded-lg shadow'>\n"
            "    <h2 className='text-xl font-bold mb-4'>Financial Analysis</h2>\n"
            "    <p className='text-gray-600'>Analysis completed. Check structured data.</p>\n"
            "  </div>\n"
            ");\n\n"
            "export default FinancialAnalysisDisplay;"
        ),
        "component_name": "FinancialAnalysisDisplay",
        "required_dependencies": ["react", "lucide-react"],
        "props_interface": "interface Props { data?: any; }",
        "generated_at": datetime.now().isoformat(),
        "framework": "React/TypeScript",
        "note": f"Fallback component: {error}",
    }
