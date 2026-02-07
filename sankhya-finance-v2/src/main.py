"""
Sankhya Finance v2 - CLI Entry Point.

Run this to interact with the LangGraph-powered financial analysis agent
from the command line.

Usage:
    # Interactive mode (asks for queries in a loop)
    python -m src.main

    # Single query mode
    python -m src.main --query "What is Apple's stock price?"

    # Debug mode (shows all node outputs and state transitions)
    python -m src.main --debug

Prerequisites:
    1. Install dependencies: pip install -r requirements.txt
    2. Set up your API key: cp .env.template .env && edit .env
"""

import asyncio
import argparse
import json
import os
import sys
from datetime import datetime

from dotenv import load_dotenv

# Load .env file before anything else
load_dotenv()

from src.graph import create_graph
from src.state import create_initial_state, StepResult, VerificationResult


# =============================================================================
# Display Helpers
# =============================================================================


def print_header():
    """Print the application header."""
    print("\n" + "=" * 60)
    print("  Sankhya Finance v2 - LangGraph Agent")
    print("  AI-Powered Financial Analysis")
    print("=" * 60)


def print_result(result: dict, debug: bool = False):
    """
    Display the final result from the graph in a readable format.

    Args:
        result: The final FinanceState dict returned by graph.ainvoke().
        debug:  If True, show all state fields and node messages.
    """
    print("\n" + "-" * 60)

    # --- Show error if any ---
    if result.get("error"):
        print(f"\n[ERROR] {result['error']}")
        return

    # --- Show structured output summary ---
    structured = result.get("structured_output", {})
    if structured:
        summary = structured.get("summary", "")
        if summary:
            print(f"\n  Summary: {summary}")

        # Show key insights
        insights = structured.get("key_insights", [])
        if insights:
            print("\n  Key Insights:")
            for i, insight in enumerate(insights, 1):
                print(f"    {i}. {insight}")

        # Show content blocks summary
        blocks = structured.get("content_blocks", [])
        if blocks:
            print(f"\n  Content Blocks: {len(blocks)}")
            for block in blocks:
                block_type = block.get("type", "unknown")
                block_title = block.get("title", "Untitled")
                print(f"    - [{block_type.upper()}] {block_title}")

                # Show metric values
                if block_type == "metric":
                    data = block.get("data", {})
                    value = data.get("value", "N/A")
                    label = data.get("label", "")
                    print(f"      {label}: {value}")

        # Show recommendations
        recs = structured.get("recommendations", [])
        if recs:
            print("\n  Recommendations:")
            for rec in recs:
                print(f"    - {rec}")

    # --- Show raw analysis if no structured output ---
    elif result.get("raw_analysis"):
        print(f"\n{result['raw_analysis']}")

    # --- Show TypeScript component info ---
    ts = result.get("typescript_component", {})
    if ts and ts.get("component_name"):
        print(f"\n  TypeScript Component: {ts['component_name']}")
        deps = ts.get("required_dependencies", [])
        if deps:
            print(f"  Dependencies: {', '.join(deps)}")
        code_len = len(ts.get("component_code", ""))
        if code_len:
            print(f"  Code Length: {code_len} chars")

    # --- Debug: show all messages and state ---
    if debug:
        print("\n" + "=" * 60)
        print("  DEBUG: Node Messages")
        print("=" * 60)
        for msg in result.get("messages", []):
            print(f"  {msg}")

        print(f"\n  Total node calls: {result.get('total_node_calls', 0)}")
        print(f"  Query type: {result.get('query_type', 'unknown')}")
        print(f"  Steps: {len(result.get('steps', []))}")
        print(f"  Detected tickers: {result.get('detected_tickers', [])}")

        # Show step results summary using typed StepResult
        step_results = result.get("step_results", {})
        if step_results:
            print(f"\n  Step Results:")
            for step_id, sr in step_results.items():
                if isinstance(sr, StepResult):
                    status = "OK" if sr.success else "FAILED"
                    if sr.error:
                        print(f"    {step_id} ({sr.step_type.value}) [{status}]: {sr.error}")
                    elif sr.analysis:
                        print(f"    {step_id} ({sr.step_type.value}) [{status}]: {sr.analysis[:100]}...")
                    elif sr.data:
                        print(f"    {step_id} ({sr.step_type.value}) [{status}]: dict with {len(sr.data)} keys")
                else:
                    print(f"    {step_id}: {type(sr).__name__}")

    print("\n" + "-" * 60)


# =============================================================================
# Main Functions
# =============================================================================


async def run_query(query: str, debug: bool = False) -> dict:
    """
    Run a single query through the LangGraph agent.

    Args:
        query: The user's natural language question.
        debug: Whether to show detailed debug output.

    Returns:
        The final FinanceState dict.
    """
    # Create the graph
    graph = create_graph()

    # Create initial state
    state = create_initial_state(query)

    print(f"\n  Query: {query}")
    print("  Processing...")

    # Run the graph
    # recursion_limit is set here as an extra safety net.
    # Each node invocation counts as 1 towards this limit.
    result = await graph.ainvoke(
        state,
        config={"recursion_limit": 40},
    )

    return result


async def interactive_mode(debug: bool = False):
    """
    Run the agent in interactive mode -- keeps asking for queries.

    Type 'quit', 'exit', or 'q' to stop.
    Type 'debug' to toggle debug mode.
    """
    print_header()
    print("\n  Type your financial question (or 'quit' to exit):\n")

    while True:
        try:
            query = input("  You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Goodbye!")
            break

        if not query:
            continue

        if query.lower() in ("quit", "exit", "q"):
            print("\n  Goodbye!")
            break

        if query.lower() == "debug":
            debug = not debug
            print(f"  Debug mode: {'ON' if debug else 'OFF'}")
            continue

        try:
            result = await run_query(query, debug)
            print_result(result, debug)
        except Exception as e:
            print(f"\n  [ERROR] {e}")
            if debug:
                import traceback
                traceback.print_exc()

        print()  # Blank line before next prompt


async def main():
    """Parse arguments and run the appropriate mode."""
    parser = argparse.ArgumentParser(
        description="Sankhya Finance v2 - LangGraph Financial Analysis Agent"
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Run a single query instead of interactive mode",
    )
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug mode (show node messages and state)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON result (for piping to other tools)",
    )

    args = parser.parse_args()

    # --- Check API key ---
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("your-"):
        print("\n  [ERROR] OPENAI_API_KEY not configured.")
        print("  Run: cp .env.template .env")
        print("  Then edit .env and add your OpenAI API key.\n")
        sys.exit(1)

    if args.query:
        # --- Single query mode ---
        result = await run_query(args.query, args.debug)

        if args.json:
            # Output as JSON for programmatic use
            # Filter out non-serializable fields
            output = {
                "query": result.get("query"),
                "query_type": result.get("query_type"),
                "structured_output": result.get("structured_output"),
                "typescript_component": result.get("typescript_component"),
                "raw_analysis": result.get("raw_analysis"),
                "error": result.get("error"),
            }
            print(json.dumps(output, indent=2, default=str))
        else:
            print_header()
            print_result(result, args.debug)
    else:
        # --- Interactive mode ---
        await interactive_mode(args.debug)


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    asyncio.run(main())
