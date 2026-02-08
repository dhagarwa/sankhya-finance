"""
Sankhya Finance v2 - LangGraph-powered Financial Analysis Agent

This package implements a multi-step financial analysis pipeline using
LangGraph's StateGraph for orchestration.

Architecture (7 nodes):
    START -> QueryRouter
               ├─ (non_financial) -> DirectResponse -> OutputFormatter -> END
               └─ (financial)     -> Decomposer -> Executor <-> Verifier
                                         ▲            │
                                         │  (replan)   ├─ OK + more steps -> AdvanceIndex -> Executor
                                         └─────────────├─ NEEDS_MORE_DATA -> Executor (retry, max 2)
                                                       ├─ REPLAN -> Decomposer (new plan, max 1)
                                                       └─ OK + all done -> OutputFormatter -> END

Key design:
    - Decomposer plans DATA + ANALYSIS steps, always ending with a final_synthesis step
    - Executor calls 21 tools across 5 data sources (YFinance, SEC EDGAR, FRED, FMP, DuckDuckGo)
    - Verifier checks every step against the ORIGINAL user query for completeness,
      correctness, relevance, and errors
    - final_synthesis step synthesizes all findings into a direct answer to the user's question
    - OutputFormatter produces structured JSON + React/TypeScript component from the synthesis
"""
