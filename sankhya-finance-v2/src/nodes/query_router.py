"""
QueryRouter Node - The entry point of the graph.

This is the FIRST node that runs after START. It classifies the user's
query as either "financial" (needs data + analysis) or "non_financial"
(can be answered directly by the LLM).

Classification rule:
    If the query mentions ANY specific company or ticker -> FINANCIAL
    If no specific company is mentioned -> NON_FINANCIAL

How it works:
    1. Sends the query to the LLM with a classification prompt
    2. LLM returns "YES" (financial) or "NO" (non-financial)
    3. Updates state with query_type = "financial" or "non_financial"

Graph routing after this node:
    financial     -> Decomposer -> Executor <-> Verifier loop -> OutputFormatter -> END
    non_financial -> DirectResponse -> OutputFormatter -> END

Examples:
    "What is Apple's stock price?"           -> financial (mentions Apple)
    "Compare MSFT and GOOGL revenue growth"  -> financial (mentions MSFT, GOOGL)
    "What is the latest news about Amazon?"  -> financial (mentions Amazon)
    "What are analysts saying about NVDA?"   -> financial (mentions NVDA)
    "What is a P/E ratio?"                   -> non_financial (no company)
    "Hello, how are you?"                    -> non_financial (greeting)
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

CLASSIFICATION_PROMPT = """Does this query mention or ask about a SPECIFIC company, stock, or ticker?

Query: "{query}"

STEP 1: Does the query mention a specific company name (like Apple, Tesla, Microsoft, Amazon, Nike) or a stock ticker (like AAPL, TSLA, MSFT)?
- If YES -> respond "YES" (we need to fetch real data for that company)
- If NO -> go to Step 2

STEP 2: Does the query ask about general financial concepts, definitions, or generic advice with no specific company?
- If YES -> respond "NO"

YES examples (mentions a specific company):
  "What is Apple's stock price?" -> YES
  "Latest news about Amazon" -> YES
  "Tell me about NVDA" -> YES
  "Is Tesla overvalued?" -> YES
  "Compare MSFT and GOOGL" -> YES
  "What are analysts saying about Netflix?" -> YES
  "Show me Nike's balance sheet" -> YES
  "What is the latest news about Apple Inc.?" -> YES

NO examples (no specific company mentioned):
  "What is a P/E ratio?" -> NO
  "How should I invest?" -> NO
  "Hello!" -> NO
  "What causes inflation?" -> NO

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
