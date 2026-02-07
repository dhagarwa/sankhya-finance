"""
QueryRouter Node - The entry point of the graph.

This is the FIRST node that runs after START. It classifies the user's
query as either "financial" (needs data + analysis) or "non_financial"
(can be answered directly by the LLM).

How it works:
    1. Sends the query to the LLM with a classification prompt
    2. LLM returns "YES" (financial) or "NO" (non-financial)
    3. Updates state with query_type = "financial" or "non_financial"

The conditional edge after this node routes to:
    - DecomposerNode     if query_type == "financial"
    - DirectResponseNode if query_type == "non_financial"

Examples:
    "What is Apple's stock price?"           -> financial
    "Compare MSFT and GOOGL revenue growth"  -> financial
    "What is a P/E ratio?"                   -> non_financial
    "Hello, how are you?"                    -> non_financial
"""

from typing import Any

from langchain_core.messages import HumanMessage

from src.state import FinanceState, QueryType
from src.utils.model_config import get_llm


# =============================================================================
# Classification Prompt
# =============================================================================
# This prompt is designed to be clear and unambiguous so the LLM gives
# a reliable YES/NO answer. We include examples for edge cases.
# =============================================================================

CLASSIFICATION_PROMPT = """You are an expert financial analyst. Determine if this user query requires real-time financial data from stock market APIs.

Query: "{query}"

Return ONLY "YES" if the query requires:
- Stock prices, market data, or financial metrics for specific companies
- Company financial statements (income, balance sheet, cash flow)
- Financial analysis, ratios, or comparisons between specific companies
- Market trends or sector analysis using real data
- Any information that needs to be fetched from financial data APIs

Return ONLY "NO" if the query is:
- General financial education or definitions (e.g., "What is a P/E ratio?")
- Generic investment advice (e.g., "How should I invest?")
- Economic concepts or explanations
- Conversational or greeting messages
- Questions answerable from general knowledge without specific company data

Examples:
  "What is Apple's current stock price?" -> YES
  "Compare MSFT and GOOGL revenues" -> YES
  "Show me Tesla's income statement" -> YES
  "What is a P/E ratio?" -> NO
  "How do I start investing?" -> NO
  "Hello!" -> NO

Response (YES or NO only):"""


# =============================================================================
# Node Function
# =============================================================================


async def query_router(state: FinanceState) -> dict[str, Any]:
    """
    Classify the query as financial or non-financial.

    This is a LangGraph node function. It:
        1. Reads state["query"]
        2. Asks the LLM to classify it
        3. Returns {"query_type": "financial" | "non_financial"} to update state

    Args:
        state: The current FinanceState.

    Returns:
        Partial state update with query_type and a progress message.
    """
    query = state["query"]

    # --- Call the LLM to classify ---
    llm = get_llm(temperature=0)  # Temperature 0 for deterministic classification
    prompt = CLASSIFICATION_PROMPT.format(query=query)

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    result = response.content.strip().upper()

    # --- Determine query type ---
    # Default to FINANCIAL if the LLM gives an unexpected answer,
    # because it's better to try fetching data than to miss a valid query.
    if result == "NO":
        query_type = QueryType.NON_FINANCIAL
    else:
        query_type = QueryType.FINANCIAL

    # --- Return state update ---
    return {
        "query_type": query_type,
        "messages": state.get("messages", []) + [
            f"[QueryRouter] Classified as: {query_type.value}"
        ],
        "total_node_calls": state.get("total_node_calls", 0) + 1,
    }


# =============================================================================
# Routing Function (used by conditional edge in graph.py)
# =============================================================================


def route_after_classification(state: FinanceState) -> str:
    """
    Conditional edge function: decide which node to go to after classification.

    Returns:
        "decomposer"       if the query needs financial data
        "direct_response"  if the query can be answered directly
    """
    if state.get("query_type") == QueryType.NON_FINANCIAL:
        return "direct_response"
    return "decomposer"
