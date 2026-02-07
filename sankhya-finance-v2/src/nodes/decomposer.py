"""
Decomposer Node - Breaks financial queries into executable steps.

This is the "planning" node. It takes the user's financial query and
produces a list of steps that the StepExecutor will execute one by one.

Each step is either:
    - DATA:     Fetch something from Yahoo Finance (specifies tool_name + parameters)
    - ANALYSIS: Ask the LLM to reason about previously fetched data

The Decomposer also runs ticker extraction to identify which companies
the user is asking about, so the LLM can generate correct tool parameters.

The VerifierNode can send execution BACK to this node (via the "replan"
verdict) if the original plan turns out to be wrong. When that happens,
the Decomposer receives the replan_reason in state and adjusts the plan.

Flow:
    QueryRouter -> [this node] -> StepExecutor -> Verifier -> ...
                                                     |
                                                     +-- "replan" --> [back to this node]
"""

import json
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.state import FinanceState, DecompositionStep, StepType, Verdict, VerificationResult
from src.utils.model_config import get_llm
from src.tools.yfinance_tools import get_tool_descriptions_for_llm
from src.tools.ticker_extractor import extract_tickers


# =============================================================================
# Decomposition Prompt
# =============================================================================
# This prompt tells the LLM what tools are available and how to structure
# the decomposition. It's the key prompt that drives the entire pipeline.
# =============================================================================

DECOMPOSITION_SYSTEM_PROMPT = """You are an expert equity research analyst with access to multiple financial data sources.

Your task is to decompose a financial query into executable steps. Each step is either:
1. **DATA** - Fetch raw data using a specific tool from the available data sources
2. **ANALYSIS** - Use reasoning to calculate, compare, or interpret data from previous steps

{tool_descriptions}

DATA SOURCE SELECTION GUIDE (use the best source for each need):

**Company Fundamentals (current snapshot)**:
  - get_key_metrics: Quick overview (P/E, margins, growth, ROE -- all from one call)
  - get_company_info: Sector, industry, business description
  - get_current_stock_price: Latest price, market cap, 52-week range

**Financial Statements (historical)**:
  - get_income_statements / get_balance_sheets / get_cash_flow_statements: YFinance data
  - get_sec_financial_data: SEC XBRL data (more authoritative for multi-year trends,
    use when you need 5-10 years of history or want official filing numbers)

**Forward-Looking / Estimates** (requires FMP_API_KEY):
  - get_analyst_estimates: Consensus EPS, revenue, EBITDA forecasts -- critical for valuation
  - get_earnings_surprises: Beat/miss history -- pattern recognition for earnings quality
  - get_company_rating: Quick financial health score (S-F scale)

**Market Sentiment & Ownership**:
  - get_analyst_recommendations: Buy/Sell/Hold consensus and recent upgrades/downgrades
  - get_institutional_holders: Top institutional owners, insider vs. institutional breakdown
  - get_options_overview: Put/call ratio as a sentiment indicator
  - get_insider_trades: SEC insider buying/selling (Form 4 filings)

**Macro & Rate Environment** (requires FRED_API_KEY):
  - get_economic_indicator: GDP, CPI, unemployment, fed funds rate, and 25+ more
  - get_treasury_yields: Yield curve with inversion detection

**Regulatory / Filings**:
  - get_sec_filings: List recent 10-K, 10-Q, 8-K filings with dates and URLs

**News & Context**:
  - get_company_news: Company-specific news from Yahoo Finance
  - web_search / web_news_search: Broader web and news search

CRITICAL RULES:
1. Create steps in logical order: DATA steps first, then ANALYSIS steps that depend on them
2. DATA steps MUST specify tool_name (exact name from the list above) and parameters
3. ANALYSIS steps MUST specify an analysis_prompt describing what to calculate/interpret
4. Each step must list its dependencies (which prior step_ids it needs data from)
5. Use the simplest possible plan -- don't fetch data you don't need
6. If comparing companies, create separate DATA steps for each company
7. For valuation questions, try to include BOTH trailing data (YFinance) AND forward estimates (FMP)
8. For macro-sensitive analysis (banks, REITs, growth stocks), include relevant economic indicators
9. Prefer SEC XBRL data (get_sec_financial_data) for long-term historical fundamental trends

{replan_context}

Return a JSON object with this EXACT structure:
{{
    "reasoning": "Brief explanation of your decomposition strategy",
    "steps": [
        {{
            "step_id": "step_1",
            "description": "What this step does",
            "step_type": "DATA",
            "tool_name": "get_current_stock_price",
            "parameters": {{"ticker": "AAPL"}},
            "depends_on": []
        }},
        {{
            "step_id": "step_2",
            "description": "Analyze the price data",
            "step_type": "ANALYSIS",
            "analysis_prompt": "Analyze the stock price data and provide insights about...",
            "depends_on": ["step_1"]
        }}
    ]
}}

Return ONLY valid JSON, no additional text."""


# =============================================================================
# Node Function
# =============================================================================


async def decomposer(state: FinanceState) -> dict[str, Any]:
    """
    Decompose a financial query into a plan of executable steps.

    This node:
        1. Extracts tickers from the query using the intelligent extractor
        2. Sends the query + available tools to the LLM
        3. Parses the LLM's JSON response into DecompositionStep objects
        4. Returns the steps and detected tickers in state

    If this node is being called as a REPLAN (VerifierNode sent us back),
    it includes the replan_reason in the prompt so the LLM can adjust.

    Args:
        state: The current FinanceState.

    Returns:
        Partial state update with steps, reasoning, and detected tickers.
    """
    query = state["query"]

    # --- Step 1: Extract tickers from the query ---
    # Use a cheaper/faster model for ticker extraction since it's a simpler task
    ticker_llm = get_llm(temperature=0, max_tokens=2048)
    detected_tickers = extract_tickers(query, ticker_llm)

    # --- Step 2: Check if this is a replan ---
    # If the VerifierNode sent us back with a "replan" verdict, include
    # the reason so the LLM knows what went wrong and can adjust.
    replan_context = ""
    verification: VerificationResult | None = state.get("verification")
    if verification and isinstance(verification, VerificationResult) and verification.verdict == Verdict.REPLAN:
        replan_reason = verification.replan_reason or "Unknown reason"
        previous_steps = state.get("steps", [])
        # Serialize previous steps for the prompt
        prev_steps_json = json.dumps(
            [s.model_dump() if isinstance(s, DecompositionStep) else s for s in previous_steps],
            indent=2, default=str
        )
        replan_context = f"""
IMPORTANT: This is a REPLAN. The previous plan failed.
Reason for replan: {replan_reason}
Previous plan that failed: {prev_steps_json}

Please create an improved plan that addresses the issue above."""

    # --- Step 3: Build the prompt ---
    tool_descriptions = get_tool_descriptions_for_llm()

    system_prompt = DECOMPOSITION_SYSTEM_PROMPT.format(
        tool_descriptions=tool_descriptions,
        replan_context=replan_context,
    )

    user_prompt = f"""Decompose this financial query into executable steps:

Query: "{query}"

Detected tickers: {detected_tickers if detected_tickers else "None detected -- you may need to identify relevant tickers from the query"}

Think about:
1. What specific data needs to be fetched?
2. Which companies are involved?
3. What time periods are relevant?
4. What calculations or comparisons are needed?

Provide the decomposition as JSON."""

    # --- Step 4: Call the LLM ---
    llm = get_llm(temperature=0.1)

    response = await llm.ainvoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ])

    # --- Step 5: Parse the JSON response ---
    response_text = response.content.strip()

    # Extract JSON from the response (handle markdown code blocks)
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.startswith("```"):
        response_text = response_text[3:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    response_text = response_text.strip()

    # If the response doesn't start with {, try to find JSON in it
    if not response_text.startswith("{"):
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            response_text = response_text[json_start:json_end]

    try:
        decomp_data = json.loads(response_text)
    except json.JSONDecodeError as e:
        # If JSON parsing fails, return an error state
        return {
            "error": f"Failed to parse decomposition JSON: {e}",
            "messages": state.get("messages", []) + [
                f"[Decomposer] ERROR: Failed to parse LLM response as JSON"
            ],
            "total_node_calls": state.get("total_node_calls", 0) + 1,
        }

    # --- Step 6: Convert to validated DecompositionStep models ---
    steps: list[DecompositionStep] = []
    validation_errors: list[str] = []

    for step_data in decomp_data.get("steps", []):
        # Map the step_type string to our StepType enum
        raw_type = step_data.get("step_type", "DATA").upper()
        try:
            step_type = StepType(raw_type)
        except ValueError:
            step_type = StepType.DATA  # Default if LLM gives unknown type

        step = DecompositionStep(
            step_id=step_data.get("step_id", f"step_{len(steps) + 1}"),
            description=step_data.get("description", ""),
            step_type=step_type,
            tool_name=step_data.get("tool_name"),
            parameters=step_data.get("parameters", {}),
            analysis_prompt=step_data.get("analysis_prompt"),
            depends_on=step_data.get("depends_on", []),
        )

        # Validate the step has required fields for its type
        validation_error = step.validate_for_execution()
        if validation_error:
            validation_errors.append(validation_error)

        steps.append(step)

    # Log validation errors but don't fail -- the verifier will catch issues
    if validation_errors:
        for err in validation_errors:
            print(f"  [Decomposer] Validation warning: {err}")

    reasoning = decomp_data.get("reasoning", "")

    # --- Return state update ---
    return {
        "steps": steps,
        "decomposition_reasoning": reasoning,
        "detected_tickers": detected_tickers,
        # Reset execution state when (re)planning
        "current_step_index": 0,
        "step_results": {},
        "current_step_error": "",
        "verification": VerificationResult(verdict=Verdict.OK),
        "retry_count": 0,
        "replan_count": state.get("replan_count", 0) + (1 if replan_context else 0),
        "messages": state.get("messages", []) + [
            f"[Decomposer] Created {len(steps)} steps. "
            f"Tickers: {detected_tickers}. "
            f"Reasoning: {reasoning[:100]}..."
        ] + (
            [f"[Decomposer] Validation warnings: {'; '.join(validation_errors)}"]
            if validation_errors else []
        ),
        "total_node_calls": state.get("total_node_calls", 0) + 1,
    }


