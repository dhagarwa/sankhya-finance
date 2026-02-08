"""
Full Pipeline Test -- runs real queries through the LangGraph agent.

For each S&P 500 company, generates a random equity analysis query,
runs it through the full graph (router -> decomposer -> executor ->
verifier -> formatter), and logs the complete debug trace.

Usage:
    # Test first 5 companies (quick smoke test)
    python -m tests.test_full_pipeline --count 5

    # Test a specific ticker
    python -m tests.test_full_pipeline --ticker AAPL

    # Test a batch (e.g., companies 20-30)
    python -m tests.test_full_pipeline --start 20 --count 10

    # Test all 504 companies (WARNING: ~$50-150 in API costs, ~2-4 hours)
    python -m tests.test_full_pipeline --all

    # Resume from where you left off (reads existing results, skips done)
    python -m tests.test_full_pipeline --count 50 --resume

Results are saved to tests/results/pipeline_results.jsonl (one JSON per line).
A summary is printed at the end.
"""

import asyncio
import argparse
import json
import os
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

# Ensure project root is on path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from src.graph import create_graph
from src.state import create_initial_state, StepResult, VerificationResult, DecompositionStep
from src.data.sp500_companies import SP500_COMPANIES

# Import query generator from same directory
import importlib.util
_qg_spec = importlib.util.spec_from_file_location(
    "query_generator", Path(__file__).parent / "query_generator.py"
)
_qg_mod = importlib.util.module_from_spec(_qg_spec)
_qg_spec.loader.exec_module(_qg_mod)
generate_query = _qg_mod.generate_query


# =============================================================================
# Config
# =============================================================================

RESULTS_DIR = PROJECT_ROOT / "tests" / "results"
RESULTS_FILE = RESULTS_DIR / "pipeline_results.jsonl"
SUMMARY_FILE = RESULTS_DIR / "pipeline_summary.json"


# =============================================================================
# Helpers
# =============================================================================


def _serialize_state(state: dict) -> dict:
    """Convert LangGraph state to JSON-serializable dict for logging."""
    out = {}
    for key, val in state.items():
        if key == "steps":
            out[key] = [
                s.model_dump() if isinstance(s, DecompositionStep) else str(s)
                for s in (val or [])
            ]
        elif key == "step_results":
            sr = {}
            for sid, sval in (val or {}).items():
                if isinstance(sval, StepResult):
                    sr[sid] = {
                        "step_type": sval.step_type.value,
                        "success": sval.success,
                        "error": sval.error,
                        "data_keys": list(sval.data.keys()) if sval.data else None,
                        "data_size": len(json.dumps(sval.data, default=str)) if sval.data else 0,
                        "analysis_full": sval.analysis if sval.analysis else None,
                    }
                else:
                    sr[sid] = str(sval)
            out[key] = sr
        elif key == "verification":
            if isinstance(val, VerificationResult):
                out[key] = {
                    "verdict": val.verdict.value,
                    "explanation": val.explanation[:200] if val.explanation else "",
                }
            else:
                out[key] = str(val)
        elif key == "structured_output":
            so = val or {}
            out[key] = {
                "has_summary": bool(so.get("summary")),
                "content_blocks": len(so.get("content_blocks", [])),
                "key_insights": so.get("key_insights", []),
                "recommendations": so.get("recommendations", []),
                "summary_preview": (so.get("summary", "") or "")[:300],
            }
        elif key == "typescript_component":
            tc = val or {}
            out[key] = {
                "has_component": bool(tc.get("component_code")),
                "code_length": len(tc.get("component_code", "")),
                "component_code": tc.get("component_code", ""),
                "component_name": tc.get("component_name", ""),
                "required_dependencies": tc.get("required_dependencies", []),
            }
        elif isinstance(val, (str, int, float, bool, type(None))):
            out[key] = val
        elif isinstance(val, list):
            out[key] = val
        elif isinstance(val, dict):
            out[key] = {str(k): str(v)[:100] for k, v in val.items()}
        else:
            out[key] = str(val)
    return out


def load_completed_tickers() -> set[str]:
    """Load tickers already tested from the results file."""
    done = set()
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        done.add(entry.get("ticker", ""))
                    except json.JSONDecodeError:
                        pass
    return done


def append_result(entry: dict):
    """Append a single result to the JSONL file."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_FILE, "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")


# =============================================================================
# Core Test Runner
# =============================================================================


async def test_single_query(
    ticker: str,
    company_name: str,
    graph,
    query_override: str | None = None,
) -> dict:
    """
    Run a single test query through the full pipeline.

    Returns a result dict with timing, success/failure, debug trace, etc.
    """
    # Generate query
    query_info = generate_query(ticker, company_name)
    query = query_override or query_info["query"]

    result_entry = {
        "ticker": ticker,
        "company": company_name,
        "query": query,
        "category": query_info["category"],
        "expected_tools": query_info["expected_tools"],
        "timestamp": datetime.now().isoformat(),
        "success": False,
        "error": None,
        "timing_seconds": 0,
        "node_calls": 0,
        "steps_planned": 0,
        "steps_succeeded": 0,
        "steps_failed": 0,
        "query_type": None,
        "detected_tickers": [],
        "has_structured_output": False,
        "has_typescript": False,
        "debug_messages": [],
        "state_snapshot": {},
    }

    start = time.time()

    try:
        # Create initial state and run the graph
        state = create_initial_state(query)
        final_state = await graph.ainvoke(state, config={"recursion_limit": 40})

        elapsed = time.time() - start
        result_entry["timing_seconds"] = round(elapsed, 2)

        # Extract results
        result_entry["query_type"] = str(final_state.get("query_type", ""))
        result_entry["detected_tickers"] = final_state.get("detected_tickers", [])
        result_entry["node_calls"] = final_state.get("total_node_calls", 0)
        result_entry["debug_messages"] = final_state.get("messages", [])

        # Count steps
        steps = final_state.get("steps", [])
        result_entry["steps_planned"] = len(steps)

        step_results = final_state.get("step_results", {})
        succeeded = sum(
            1 for sr in step_results.values()
            if isinstance(sr, StepResult) and sr.success
        )
        failed = sum(
            1 for sr in step_results.values()
            if isinstance(sr, StepResult) and not sr.success
        )
        result_entry["steps_succeeded"] = succeeded
        result_entry["steps_failed"] = failed

        # Check outputs
        structured = final_state.get("structured_output", {})
        result_entry["has_structured_output"] = bool(
            structured and structured.get("summary")
        )

        ts_component = final_state.get("typescript_component", {})
        result_entry["has_typescript"] = bool(
            ts_component and ts_component.get("component_code")
        )

        # Check for errors
        error = final_state.get("error", "")
        if error:
            result_entry["error"] = error
        else:
            result_entry["success"] = True

        # Serialize state snapshot for deep debugging
        result_entry["state_snapshot"] = _serialize_state(final_state)

    except Exception as e:
        elapsed = time.time() - start
        result_entry["timing_seconds"] = round(elapsed, 2)
        result_entry["error"] = f"{type(e).__name__}: {str(e)}"
        result_entry["error_traceback"] = traceback.format_exc()

    return result_entry


# =============================================================================
# Batch Runner
# =============================================================================


async def run_batch(
    tickers: list[tuple[str, str]],
    resume: bool = False,
):
    """
    Run tests for a batch of (ticker, company_name) pairs.

    Prints live progress and saves results incrementally.
    """
    # Skip already-completed tickers if resuming
    completed = load_completed_tickers() if resume else set()
    remaining = [(t, n) for t, n in tickers if t not in completed]

    if resume and len(completed) > 0:
        print(f"  Resuming: {len(completed)} already done, {len(remaining)} remaining")

    if not remaining:
        print("  All tickers already tested. Nothing to do.")
        return

    # Create graph once (reuse across queries)
    print("  Compiling LangGraph...")
    graph = create_graph()

    total = len(remaining)
    successes = 0
    failures = 0
    total_time = 0

    print(f"  Running {total} queries...\n")
    print(f"  {'#':>4}  {'Ticker':8s}  {'Category':20s}  {'Time':>6s}  {'Steps':>5s}  {'Status'}")
    print(f"  {'─'*4}  {'─'*8}  {'─'*20}  {'─'*6}  {'─'*5}  {'─'*30}")

    for i, (ticker, company_name) in enumerate(remaining, 1):
        result = await test_single_query(ticker, company_name, graph)

        # Save incrementally
        append_result(result)

        # Track stats
        total_time += result["timing_seconds"]
        if result["success"]:
            successes += 1
            status = "PASS"
        else:
            failures += 1
            err = result.get("error", "unknown")[:40]
            status = f"FAIL: {err}"

        steps_str = f"{result['steps_succeeded']}/{result['steps_planned']}"

        print(
            f"  {i:>4}  {ticker:8s}  {result['category']:20s}  "
            f"{result['timing_seconds']:5.1f}s  {steps_str:>5s}  {status}"
        )

    # Print summary
    print(f"\n  {'='*70}")
    print(f"  SUMMARY")
    print(f"  {'='*70}")
    print(f"  Total tested:  {total}")
    print(f"  Passed:        {successes} ({successes/total*100:.1f}%)")
    print(f"  Failed:        {failures} ({failures/total*100:.1f}%)")
    print(f"  Total time:    {total_time:.1f}s ({total_time/total:.1f}s avg per query)")
    print(f"  Results saved:  {RESULTS_FILE}")

    # Save summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_tested": total,
        "passed": successes,
        "failed": failures,
        "pass_rate_pct": round(successes / total * 100, 1) if total else 0,
        "total_time_seconds": round(total_time, 1),
        "avg_time_seconds": round(total_time / total, 1) if total else 0,
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(SUMMARY_FILE, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  Summary saved:  {SUMMARY_FILE}")


# =============================================================================
# CLI
# =============================================================================


async def main():
    parser = argparse.ArgumentParser(
        description="Full pipeline test for Sankhya Finance v2"
    )
    parser.add_argument("--ticker", "-t", type=str, help="Test a specific ticker")
    parser.add_argument("--query", "-q", type=str, help="Override query text (use with --ticker)")
    parser.add_argument("--count", "-n", type=int, default=5, help="Number of companies to test (default: 5)")
    parser.add_argument("--start", "-s", type=int, default=0, help="Start index in sorted ticker list")
    parser.add_argument("--all", action="store_true", help="Test ALL 504 companies")
    parser.add_argument("--resume", "-r", action="store_true", help="Skip already-tested tickers")
    parser.add_argument("--sector", type=str, help="Test only companies in this sector")
    parser.add_argument("--clear", action="store_true", help="Clear previous results before running")

    args = parser.parse_args()

    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("your-"):
        print("\n  [ERROR] OPENAI_API_KEY not configured.")
        sys.exit(1)

    # Clear previous results if requested
    if args.clear and RESULTS_FILE.exists():
        RESULTS_FILE.unlink()
        print("  Cleared previous results.")

    if args.ticker:
        # --- Single ticker mode ---
        ticker = args.ticker.upper()
        info = SP500_COMPANIES.get(ticker)
        if not info:
            print(f"  [ERROR] Ticker {ticker} not found in SP500 database")
            sys.exit(1)

        print(f"\n  Testing: {ticker} ({info['name']})")
        graph = create_graph()
        result = await test_single_query(
            ticker, info["name"], graph,
            query_override=args.query,
        )

        # Print detailed result
        print(f"\n  Query:    {result['query']}")
        print(f"  Category: {result['category']}")
        print(f"  Status:   {'PASS' if result['success'] else 'FAIL'}")
        print(f"  Time:     {result['timing_seconds']}s")
        print(f"  Tickers:  {result['detected_tickers']}")
        print(f"  Steps:    {result['steps_succeeded']}/{result['steps_planned']} succeeded")
        print(f"  Output:   structured={'yes' if result['has_structured_output'] else 'no'}, "
              f"typescript={'yes' if result['has_typescript'] else 'no'}")

        if result.get("error"):
            print(f"  Error:    {result['error']}")

        print(f"\n  Debug Messages:")
        for msg in result.get("debug_messages", []):
            print(f"    {msg}")

        # Show structured output preview
        snap = result.get("state_snapshot", {})
        so = snap.get("structured_output", {})
        if so.get("summary_preview"):
            print(f"\n  Output Summary: {so['summary_preview']}")
            print(f"  Content Blocks: {so.get('content_blocks', 0)}")
            print(f"  Key Insights:   {so.get('key_insights', 0)}")

        append_result(result)
        print(f"\n  Result saved to {RESULTS_FILE}")

    else:
        # --- Batch mode ---
        all_tickers = sorted(SP500_COMPANIES.items())

        if args.sector:
            all_tickers = [
                (t, i) for t, i in all_tickers
                if i["sector"].lower() == args.sector.lower()
            ]
            print(f"\n  Filtered to sector '{args.sector}': {len(all_tickers)} companies")

        # Convert to (ticker, name) pairs
        ticker_pairs = [(t, i["name"]) for t, i in all_tickers]

        if args.all:
            batch = ticker_pairs
            print(f"\n  Testing ALL {len(batch)} companies")
        else:
            batch = ticker_pairs[args.start:args.start + args.count]
            print(f"\n  Testing {len(batch)} companies (index {args.start} to {args.start + len(batch) - 1})")

        await run_batch(batch, resume=args.resume)


if __name__ == "__main__":
    asyncio.run(main())
