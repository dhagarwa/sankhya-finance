"""
LangGraph StateGraph Definition - The heart of Sankhya Finance v2.

This module wires together all the nodes, edges, and conditional routing
into a single compiled LangGraph graph. This is the ONE file that defines
the complete execution flow of the agent.

Graph Structure:
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │  START                                                      │
    │    │                                                        │
    │    ▼                                                        │
    │  QueryRouter                                                │
    │    │                                                        │
    │    ├──(non_financial)──► DirectResponse ──► OutputFormatter  │
    │    │                                           │            │
    │    └──(financial)──► Decomposer ◄──────────────┤            │
    │                        │              (replan)  │            │
    │                        ▼                        │            │
    │                    Executor ◄────────┐          │            │
    │                        │             │          │            │
    │                        ▼             │          │            │
    │                    Verifier ─────────┘          │            │
    │                        │  (needs_more_data)     │            │
    │                        │                        │            │
    │                        ├──(ok, more steps)──► AdvanceIndex   │
    │                        │                        │            │
    │                        │                        ▼            │
    │                        │                    Executor         │
    │                        │                                    │
    │                        └──(ok, all done)──► OutputFormatter  │
    │                                                 │            │
    │                                                 ▼            │
    │                                               END            │
    └─────────────────────────────────────────────────────────────┘

Usage:
    from src.graph import create_graph
    from src.state import create_initial_state

    graph = create_graph()
    state = create_initial_state("What is Apple's stock price?")
    result = await graph.ainvoke(state)
"""

from langgraph.graph import StateGraph, START, END

from src.state import FinanceState

# --- Import all node functions ---
from src.nodes.query_router import query_router, route_after_classification
from src.nodes.direct_response import direct_response
from src.nodes.decomposer import decomposer
from src.nodes.step_executor import step_executor
from src.nodes.verifier import verifier, route_after_verification, advance_step_index
from src.nodes.output_formatter import output_formatter


# =============================================================================
# Graph Construction
# =============================================================================


def create_graph() -> StateGraph:
    """
    Build and compile the Sankhya Finance LangGraph.

    This function:
        1. Creates a StateGraph with FinanceState as the schema
        2. Adds all 7 nodes (router, direct_response, decomposer,
           executor, verifier, advance_index, output_formatter)
        3. Wires edges and conditional edges between them
        4. Compiles the graph with a recursion limit for safety

    Returns:
        A compiled LangGraph ready for .invoke() or .ainvoke().

    Example:
        graph = create_graph()
        result = await graph.ainvoke({"query": "What is AAPL's stock price?"})
    """

    # --- 1. Create the graph with our state schema ---
    workflow = StateGraph(FinanceState)

    # --- 2. Add all nodes ---
    # Each node is an async function that takes FinanceState and returns
    # a partial dict to update the state.

    workflow.add_node("query_router", query_router)
    workflow.add_node("direct_response", direct_response)
    workflow.add_node("decomposer", decomposer)
    workflow.add_node("executor", step_executor)
    workflow.add_node("verifier", verifier)
    workflow.add_node("advance_and_execute", advance_step_index)
    workflow.add_node("output_formatter", output_formatter)

    # --- 3. Wire the edges ---

    # START -> QueryRouter (always the first node)
    workflow.add_edge(START, "query_router")

    # QueryRouter -> (conditional) DirectResponse OR Decomposer
    workflow.add_conditional_edges(
        "query_router",
        route_after_classification,
        {
            "direct_response": "direct_response",
            "decomposer": "decomposer",
        },
    )

    # DirectResponse -> OutputFormatter (skip the whole execute/verify loop)
    workflow.add_edge("direct_response", "output_formatter")

    # Decomposer -> Executor (start executing the plan)
    workflow.add_edge("decomposer", "executor")

    # Executor -> Verifier (always verify after executing)
    workflow.add_edge("executor", "verifier")

    # Verifier -> (conditional) multiple destinations
    # This is the KEY conditional edge that enables self-correction:
    #   - "needs_more_data" -> back to executor (retry with modified step)
    #   - "replan"          -> back to decomposer (create new plan)
    #   - "advance_and_execute" -> increment step index, then executor
    #   - "output_formatter"    -> all done, produce final output
    workflow.add_conditional_edges(
        "verifier",
        route_after_verification,
        {
            "executor": "executor",               # retry current step
            "decomposer": "decomposer",           # replan
            "advance_and_execute": "advance_and_execute",  # next step
            "output_formatter": "output_formatter",         # all done
        },
    )

    # AdvanceAndExecute -> Executor (after incrementing index)
    workflow.add_edge("advance_and_execute", "executor")

    # OutputFormatter -> END (terminal node)
    workflow.add_edge("output_formatter", END)

    # --- 4. Compile with safety limit ---
    # recursion_limit prevents infinite loops if verifier keeps retrying.
    # 40 is generous: a typical query with 5 steps would use ~15 node calls
    # (router + decomposer + 5*(executor + verifier + advance) + formatter).
    graph = workflow.compile()

    return graph


# =============================================================================
# Convenience: Pre-built graph instance
# =============================================================================
# Import this for quick usage:
#   from src.graph import finance_graph
#   result = await finance_graph.ainvoke(state)
# =============================================================================

# We don't pre-compile here because it would import all nodes at module load.
# Instead, call create_graph() when you need it.
