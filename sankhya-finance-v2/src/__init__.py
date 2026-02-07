"""
Sankhya Finance v2 - LangGraph-powered Financial Analysis Agent

This package implements a multi-step financial analysis pipeline using
LangGraph's StateGraph for orchestration. The graph decomposes user queries
into executable steps, fetches data from Yahoo Finance, runs LLM-powered
analysis, verifies results, and produces structured output.

Architecture:
    START -> QueryRouter -> [DecomposerNode | DirectResponseNode]
          -> StepExecutorNode <-> VerifierNode (cycles)
          -> OutputFormatterNode -> END
"""
