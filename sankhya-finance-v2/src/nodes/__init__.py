"""
Graph Nodes - Each file in this package is a LangGraph node.

Nodes are pure functions that take FinanceState as input and return
a partial state update dict. They are wired together in graph.py.

Node overview:
    - query_router:     Classifies queries as financial vs non-financial
    - direct_response:  Handles non-financial queries with a single LLM call
    - decomposer:       Breaks financial queries into DATA/ANALYSIS steps
    - step_executor:    Executes one step at a time (YFinance calls or LLM analysis)
    - verifier:         Checks step results, can send execution back to retry/replan
    - output_formatter: Produces structured JSON + TypeScript React components
"""
