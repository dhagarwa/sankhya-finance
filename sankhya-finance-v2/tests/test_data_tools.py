"""
Data Tools Coverage Test -- tests raw tool calls against S&P 500 tickers.

NO LLM calls, NO API key costs (except FRED/FMP if configured).
Tests whether each data tool returns valid data for each ticker.

This is the fast, cheap first pass before running full pipeline tests.

Usage:
    # Quick test: 3 tools x 10 tickers (30 calls, ~30 seconds)
    python -m tests.test_data_tools --count 10

    # Test a specific tool across all tickers
    python -m tests.test_data_tools --tool get_current_stock_price --all

    # Test all free tools (no API key) for all tickers
    python -m tests.test_data_tools --all --free-only

    # Test a specific ticker against all tools
    python -m tests.test_data_tools --ticker AAPL

Results saved to tests/results/tools_results.jsonl
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from src.data.sp500_companies import SP500_COMPANIES
from src.tools.yfinance_tools import TOOLS_BY_NAME

RESULTS_DIR = PROJECT_ROOT / "tests" / "results"
RESULTS_FILE = RESULTS_DIR / "tools_results.jsonl"


# =============================================================================
# Tool Test Definitions
# =============================================================================
# For each tool, define the default parameters to use and whether it's free.

TOOL_TEST_CONFIGS = {
    # --- YFinance (free, no API key) ---
    "get_current_stock_price": {
        "params": lambda t: {"ticker": t},
        "free": True,
        "fast": True,
    },
    "get_key_metrics": {
        "params": lambda t: {"ticker": t},
        "free": True,
        "fast": True,
    },
    "get_company_info": {
        "params": lambda t: {"ticker": t},
        "free": True,
        "fast": True,
    },
    "get_income_statements": {
        "params": lambda t: {"ticker": t, "period": "annual", "limit": 3},
        "free": True,
        "fast": True,
    },
    "get_balance_sheets": {
        "params": lambda t: {"ticker": t, "period": "annual", "limit": 3},
        "free": True,
        "fast": True,
    },
    "get_cash_flow_statements": {
        "params": lambda t: {"ticker": t, "period": "annual", "limit": 3},
        "free": True,
        "fast": True,
    },
    "get_historical_stock_prices": {
        "params": lambda t: {"ticker": t, "start_date": "2025-01-01", "end_date": "2025-06-01"},
        "free": True,
        "fast": True,
    },
    "get_company_news": {
        "params": lambda t: {"ticker": t, "limit": 3},
        "free": True,
        "fast": True,
    },
    "get_analyst_recommendations": {
        "params": lambda t: {"ticker": t},
        "free": True,
        "fast": True,
    },
    "get_institutional_holders": {
        "params": lambda t: {"ticker": t},
        "free": True,
        "fast": True,
    },
    "get_options_overview": {
        "params": lambda t: {"ticker": t},
        "free": True,
        "fast": True,
    },

    # --- SEC EDGAR (free, no API key) ---
    "get_sec_filings": {
        "params": lambda t: {"ticker": t, "filing_type": "10-K", "limit": 3},
        "free": True,
        "fast": False,  # SEC rate limited
    },
    "get_sec_financial_data": {
        "params": lambda t: {"ticker": t, "metrics": "revenue,net_income,eps"},
        "free": True,
        "fast": False,
    },
    "get_insider_trades": {
        "params": lambda t: {"ticker": t, "limit": 5},
        "free": True,
        "fast": False,
    },

    # --- FRED (requires free API key) ---
    "get_economic_indicator": {
        "params": lambda t: {"indicator": "fed_funds_rate", "limit": 5},
        "free": False,  # needs FRED_API_KEY
        "fast": True,
        "ticker_independent": True,  # same result for all tickers
    },
    "get_treasury_yields": {
        "params": lambda t: {},
        "free": False,
        "fast": True,
        "ticker_independent": True,
    },

    # --- FMP (requires free API key) ---
    "get_analyst_estimates": {
        "params": lambda t: {"ticker": t, "period": "annual", "limit": 3},
        "free": False,  # needs FMP_API_KEY
        "fast": True,
    },
    "get_company_rating": {
        "params": lambda t: {"ticker": t},
        "free": False,
        "fast": True,
    },
    "get_earnings_surprises": {
        "params": lambda t: {"ticker": t, "limit": 4},
        "free": False,
        "fast": True,
    },

    # --- Web Search (free) ---
    "web_search": {
        "params": lambda t: {"query": f"{t} stock analysis", "max_results": 2},
        "free": True,
        "fast": True,
    },
    "web_news_search": {
        "params": lambda t: {"query": f"{t} earnings", "max_results": 2},
        "free": True,
        "fast": True,
    },
}


# =============================================================================
# Test Runner
# =============================================================================


def test_tool(tool_name: str, ticker: str) -> dict:
    """Test a single tool with a single ticker. Returns result dict."""
    config = TOOL_TEST_CONFIGS.get(tool_name)
    if not config:
        return {"tool": tool_name, "ticker": ticker, "error": "Unknown tool", "success": False}

    tool_fn = TOOLS_BY_NAME.get(tool_name)
    if not tool_fn:
        return {"tool": tool_name, "ticker": ticker, "error": "Tool not in TOOLS_BY_NAME", "success": False}

    params = config["params"](ticker)
    start = time.time()

    try:
        result = tool_fn.invoke(params)
        elapsed = round(time.time() - start, 2)

        has_error = isinstance(result, dict) and "error" in result
        return {
            "tool": tool_name,
            "ticker": ticker,
            "success": not has_error,
            "error": result.get("error") if has_error else None,
            "result_keys": list(result.keys()) if isinstance(result, dict) else None,
            "result_size": len(json.dumps(result, default=str)),
            "timing_seconds": elapsed,
        }
    except Exception as e:
        elapsed = round(time.time() - start, 2)
        return {
            "tool": tool_name,
            "ticker": ticker,
            "success": False,
            "error": f"{type(e).__name__}: {str(e)}",
            "timing_seconds": elapsed,
        }


def run_tests(
    tickers: list[str],
    tools: list[str],
    save: bool = True,
) -> dict:
    """
    Run tools against tickers and collect results.

    Returns a summary dict.
    """
    total = len(tickers) * len(tools)
    passes = 0
    fails = 0
    errors_by_tool: dict[str, int] = {}
    errors_by_ticker: dict[str, int] = {}
    all_results = []

    print(f"  Testing {len(tools)} tools x {len(tickers)} tickers = {total} calls\n")
    print(f"  {'Tool':35s}  {'Pass':>5s}  {'Fail':>5s}  {'Avg Time':>8s}")
    print(f"  {'─'*35}  {'─'*5}  {'─'*5}  {'─'*8}")

    for tool_name in tools:
        config = TOOL_TEST_CONFIGS.get(tool_name, {})
        tool_passes = 0
        tool_fails = 0
        tool_times = []

        # For ticker-independent tools (FRED), only test once
        test_tickers = ["N/A"] if config.get("ticker_independent") else tickers

        for ticker in test_tickers:
            result = test_tool(tool_name, ticker)
            all_results.append(result)

            if result["success"]:
                tool_passes += 1
                passes += 1
            else:
                tool_fails += 1
                fails += 1
                errors_by_tool[tool_name] = errors_by_tool.get(tool_name, 0) + 1
                if ticker != "N/A":
                    errors_by_ticker[ticker] = errors_by_ticker.get(ticker, 0) + 1

            tool_times.append(result.get("timing_seconds", 0))

        avg_time = sum(tool_times) / len(tool_times) if tool_times else 0
        status = f"{tool_passes:>5d}  {tool_fails:>5d}  {avg_time:>7.2f}s"
        print(f"  {tool_name:35s}  {status}")

    # Save results
    if save:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        with open(RESULTS_FILE, "w") as f:
            for r in all_results:
                f.write(json.dumps(r, default=str) + "\n")

    # Print summary
    total_actual = passes + fails
    print(f"\n  {'='*60}")
    print(f"  SUMMARY")
    print(f"  {'='*60}")
    print(f"  Total calls:  {total_actual}")
    print(f"  Passed:       {passes} ({passes/total_actual*100:.1f}%)" if total_actual else "")
    print(f"  Failed:       {fails} ({fails/total_actual*100:.1f}%)" if total_actual else "")

    if errors_by_tool:
        print(f"\n  Failures by tool:")
        for tool, count in sorted(errors_by_tool.items(), key=lambda x: -x[1]):
            print(f"    {tool}: {count} failures")

    if errors_by_ticker:
        top_failing = sorted(errors_by_ticker.items(), key=lambda x: -x[1])[:10]
        print(f"\n  Top failing tickers:")
        for ticker, count in top_failing:
            print(f"    {ticker}: {count} tool failures")

    if save:
        print(f"\n  Results saved: {RESULTS_FILE}")

    return {
        "total": total_actual,
        "passed": passes,
        "failed": fails,
        "errors_by_tool": errors_by_tool,
    }


# =============================================================================
# CLI
# =============================================================================


def main():
    parser = argparse.ArgumentParser(description="Data tools coverage test")
    parser.add_argument("--ticker", "-t", type=str, help="Test a specific ticker against all tools")
    parser.add_argument("--tool", type=str, help="Test a specific tool against tickers")
    parser.add_argument("--count", "-n", type=int, default=10, help="Number of tickers to test (default: 10)")
    parser.add_argument("--start", "-s", type=int, default=0, help="Start index")
    parser.add_argument("--all", action="store_true", help="Test all 504 tickers")
    parser.add_argument("--free-only", action="store_true", help="Only test tools that need no API key")
    parser.add_argument("--fast-only", action="store_true", help="Only test fast tools (skip SEC rate-limited)")
    parser.add_argument("--sector", type=str, help="Test only this sector")

    args = parser.parse_args()

    # Determine tools to test
    if args.tool:
        tools = [args.tool]
    else:
        tools = list(TOOL_TEST_CONFIGS.keys())
        if args.free_only:
            tools = [t for t in tools if TOOL_TEST_CONFIGS[t].get("free")]
        if args.fast_only:
            tools = [t for t in tools if TOOL_TEST_CONFIGS[t].get("fast")]

    # Determine tickers to test
    if args.ticker:
        tickers = [args.ticker.upper()]
    else:
        all_tickers = sorted(SP500_COMPANIES.keys())
        if args.sector:
            all_tickers = [
                t for t in all_tickers
                if SP500_COMPANIES[t]["sector"].lower() == args.sector.lower()
            ]
        if args.all:
            tickers = all_tickers
        else:
            tickers = all_tickers[args.start:args.start + args.count]

    print(f"\n  Sankhya Finance v2 - Data Tools Coverage Test")
    print(f"  {'='*50}")
    print(f"  Tickers: {len(tickers)} | Tools: {len(tools)}")
    if args.free_only:
        print(f"  Mode: free tools only (no API keys needed)")
    print()

    run_tests(tickers, tools)


if __name__ == "__main__":
    main()
