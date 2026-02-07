"""
DirectResponse Node - Handles non-financial queries.

This node runs when the QueryRouter classifies a query as "non_financial".
Instead of going through the full decompose -> execute -> verify pipeline,
it gives a direct LLM response and sends it straight to the OutputFormatter.

Examples of queries this handles:
    - "What is a P/E ratio?"
    - "How does compound interest work?"
    - "Hello, can you help me?"
    - "What's the difference between stocks and bonds?"

The response is stored in state["direct_response"] and state["raw_analysis"],
which the OutputFormatter will pick up to produce structured output.
"""

from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.state import FinanceState
from src.utils.model_config import get_llm


# =============================================================================
# System Prompt
# =============================================================================
# Tells the LLM to act as Sankhya Finance and provide helpful financial
# education without needing real-time data.
# =============================================================================

SYSTEM_PROMPT = """You are Sankhya Finance, an AI-powered financial analysis assistant.

The user has asked a question that doesn't require real-time market data or specific company financials. Provide a helpful, educational, and comprehensive response.

Guidelines:
- If it's a financial concept, explain it clearly with examples
- If it's investment advice, provide general educational guidance (not specific recommendations)
- If it's a greeting, respond warmly and explain what you can help with
- Keep responses informative but concise (2-4 paragraphs)
- End by mentioning you can also help with specific company analysis, stock prices, and financial data"""


# =============================================================================
# Node Function
# =============================================================================


async def direct_response(state: FinanceState) -> dict[str, Any]:
    """
    Generate a direct LLM response for non-financial queries.

    This node:
        1. Reads state["query"]
        2. Sends it to the LLM with the Sankhya Finance persona
        3. Returns the response in state["direct_response"] and state["raw_analysis"]

    After this node, the graph goes straight to OutputFormatterNode
    (skipping decomposer, executor, and verifier).

    Args:
        state: The current FinanceState.

    Returns:
        Partial state update with the direct response.
    """
    query = state["query"]

    # --- Call the LLM ---
    llm = get_llm(temperature=0.3)  # Slightly creative for educational content

    response = await llm.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=query),
    ])

    answer = response.content

    # --- Return state update ---
    return {
        "direct_response": answer,
        "raw_analysis": answer,  # OutputFormatter reads this field
        "messages": state.get("messages", []) + [
            f"[DirectResponse] Generated direct answer ({len(answer)} chars)"
        ],
        "total_node_calls": state.get("total_node_calls", 0) + 1,
    }
