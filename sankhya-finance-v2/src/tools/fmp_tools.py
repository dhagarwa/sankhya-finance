"""
Financial Modeling Prep (FMP) Tools for LangGraph.

Provides access to FMP's free-tier API for data that YFinance and SEC
EDGAR don't provide well:
    - Analyst consensus estimates (forward EPS, revenue forecasts)
    - Company financial health ratings
    - Earnings surprises (actual vs. estimated EPS)

These fill a critical gap: YFinance gives you trailing data, but equity
analysis needs FORWARD estimates to value stocks. Analyst consensus is
the standard source for forward-looking data.

Uses FMP's /stable/ API (the current production API).

Requires: FMP_API_KEY (free tier: ~250 calls/day)
Register at: https://financialmodelingprep.com/developer/docs/

If the API key is not set, tools return a helpful error message with
the registration URL instead of crashing.
"""

import os
from typing import Any

import requests
from langchain_core.tools import tool


# =============================================================================
# Configuration
# =============================================================================

FMP_BASE = "https://financialmodelingprep.com/stable"


def _get_fmp_key() -> str | None:
    """Get FMP API key from environment."""
    return os.getenv("FMP_API_KEY")


def _fmp_get(endpoint: str, params: dict | None = None) -> Any:
    """Make a request to the FMP stable API."""
    api_key = _get_fmp_key()
    if not api_key:
        raise EnvironmentError(
            "FMP_API_KEY not set. Get a free key (250 calls/day) at: "
            "https://financialmodelingprep.com/developer/docs/  "
            "Then add FMP_API_KEY=your-key to your .env file."
        )

    if params is None:
        params = {}
    params["apikey"] = api_key

    resp = requests.get(f"{FMP_BASE}/{endpoint}", params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


# =============================================================================
# Tool Implementations
# =============================================================================


@tool
def get_analyst_estimates(
    ticker: str,
    period: str = "annual",
    limit: int = 5,
) -> dict[str, Any]:
    """Get Wall Street analyst consensus estimates for a company.

    Returns forward-looking estimates for revenue, EPS, EBITDA, net income
    -- including low, average, and high estimates for each period.

    This is CRITICAL for equity analysis: forward P/E, PEG ratio, and
    DCF models all depend on analyst estimates.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
        period: 'annual' or 'quarter' (default: 'annual').
        limit: Number of periods to return (default: 5).
    """
    try:
        data = _fmp_get("analyst-estimates", {
            "symbol": ticker.upper(),
            "period": period,
            "limit": limit,
        })

        if not data:
            return {"error": f"No analyst estimates found for {ticker}"}

        if isinstance(data, dict) and "Error Message" in data:
            return {"error": f"FMP API error: {data['Error Message']}"}

        # Clean and structure the response
        estimates = []
        for entry in data:
            estimates.append({
                "date": entry.get("date", ""),
                "revenue_estimate": {
                    "low": entry.get("revenueLow"),
                    "avg": entry.get("revenueAvg"),
                    "high": entry.get("revenueHigh"),
                },
                "eps_estimate": {
                    "low": entry.get("epsLow") or entry.get("estimatedEpsLow"),
                    "avg": entry.get("epsAvg") or entry.get("estimatedEpsAvg"),
                    "high": entry.get("epsHigh") or entry.get("estimatedEpsHigh"),
                },
                "ebitda_estimate": {
                    "low": entry.get("ebitdaLow") or entry.get("estimatedEbitdaLow"),
                    "avg": entry.get("ebitdaAvg") or entry.get("estimatedEbitdaAvg"),
                    "high": entry.get("ebitdaHigh") or entry.get("estimatedEbitdaHigh"),
                },
                "net_income_estimate": {
                    "low": entry.get("netIncomeLow") or entry.get("estimatedNetIncomeLow"),
                    "avg": entry.get("netIncomeAvg") or entry.get("estimatedNetIncomeAvg"),
                    "high": entry.get("netIncomeHigh") or entry.get("estimatedNetIncomeHigh"),
                },
                "number_of_analysts": entry.get("numberAnalystsEstimatedRevenue") or entry.get("numberAnalystEstimatedRevenue"),
            })

        return {
            "ticker": ticker.upper(),
            "period": period,
            "estimate_count": len(estimates),
            "estimates": estimates,
            "note": "Estimates reflect Wall Street consensus. "
                    "'avg' is the consensus estimate, 'low'/'high' show the range of analyst views.",
        }

    except EnvironmentError as e:
        return {"error": str(e)}
    except requests.exceptions.HTTPError as e:
        return {"error": f"FMP API error for {ticker}: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to fetch analyst estimates for {ticker}: {str(e)}"}


@tool
def get_company_rating(ticker: str) -> dict[str, Any]:
    """Get a quantitative financial health rating for a company.

    Returns an overall rating (A to F scale) based on DCF analysis, ROE,
    ROA, D/E ratio, P/E, and P/B. Also provides individual scores for
    each category.

    Useful as a quick screening tool before deeper analysis.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        data = _fmp_get("ratings-snapshot", {"symbol": ticker.upper()})

        if not data:
            return {"error": f"No rating data found for {ticker}"}

        if isinstance(data, dict) and "Error Message" in data:
            return {"error": f"FMP API error: {data['Error Message']}"}

        # FMP returns a list; take the most recent
        rating = data[0] if isinstance(data, list) else data

        return {
            "ticker": ticker.upper(),
            "overall_rating": rating.get("rating", ""),
            "overall_score": rating.get("overallScore"),
            "recommendation": rating.get("ratingRecommendation", ""),
            "component_scores": {
                "dcf": rating.get("discountedCashFlowScore"),
                "roe": rating.get("returnOnEquityScore"),
                "roa": rating.get("returnOnAssetsScore"),
                "debt_to_equity": rating.get("debtToEquityScore"),
                "pe": rating.get("priceToEarningsScore"),
                "pb": rating.get("priceToBookScore"),
            },
            "note": "Scores range from 1 (worst) to 5 (best). "
                    "Overall rating: A=strong, B=good, C=fair, D=weak, F=poor.",
        }

    except EnvironmentError as e:
        return {"error": str(e)}
    except requests.exceptions.HTTPError as e:
        return {"error": f"FMP API error for {ticker}: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to fetch company rating for {ticker}: {str(e)}"}


@tool
def get_earnings_surprises(ticker: str, limit: int = 8) -> dict[str, Any]:
    """Get historical earnings surprises (actual vs. estimated EPS).

    Shows whether a company has been beating or missing earnings estimates.
    A pattern of beats/misses is a strong signal for equity analysis:
    - Consistent beats suggest conservative guidance or accelerating business
    - Consistent misses suggest structural problems or overly optimistic estimates

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
        limit: Number of quarters to return (default: 8, i.e., 2 years).
    """
    try:
        data = _fmp_get("earnings", {"symbol": ticker.upper()})

        if not data:
            return {"error": f"No earnings data found for {ticker}"}

        if isinstance(data, dict) and "Error Message" in data:
            return {"error": f"FMP API error: {data['Error Message']}"}

        # Filter to entries that have actual data (skip future dates)
        entries_with_data = [
            e for e in data
            if e.get("epsActual") is not None
        ][:limit]

        surprises = []
        beats = 0
        misses = 0
        total = 0
        for entry in entries_with_data:
            actual = entry.get("epsActual")
            estimated = entry.get("epsEstimated")

            surprise_pct = None
            result = "N/A"
            if actual is not None and estimated is not None and estimated != 0:
                surprise_pct = round(((actual - estimated) / abs(estimated)) * 100, 2)
                if actual > estimated:
                    result = "BEAT"
                    beats += 1
                elif actual < estimated:
                    result = "MISS"
                    misses += 1
                else:
                    result = "IN_LINE"
                total += 1

            surprises.append({
                "date": entry.get("date", ""),
                "actual_eps": actual,
                "estimated_eps": estimated,
                "revenue_actual": entry.get("revenueActual"),
                "revenue_estimated": entry.get("revenueEstimated"),
                "surprise_pct": surprise_pct,
                "result": result,
            })

        summary = {}
        if total > 0:
            summary = {
                "quarters_analyzed": total,
                "beats": beats,
                "misses": misses,
                "in_line": total - beats - misses,
                "beat_rate_pct": round((beats / total) * 100, 1),
            }

        return {
            "ticker": ticker.upper(),
            "surprise_count": len(surprises),
            "summary": summary,
            "surprises": surprises,
        }

    except EnvironmentError as e:
        return {"error": str(e)}
    except requests.exceptions.HTTPError as e:
        return {"error": f"FMP API error for {ticker}: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to fetch earnings surprises for {ticker}: {str(e)}"}


# =============================================================================
# Tool Registry (for the Decomposer to describe to the LLM)
# =============================================================================

FMP_TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    "get_analyst_estimates": {
        "description": "Get Wall Street analyst consensus estimates (forward EPS, revenue, EBITDA forecasts). Critical for forward P/E and valuation. Requires FMP_API_KEY (free tier: 250 calls/day).",
        "parameters": {
            "ticker": "Stock ticker symbol (e.g., 'AAPL')",
            "period": "'annual' or 'quarter' (default: 'annual')",
            "limit": "Number of periods (default: 5)",
        },
    },
    "get_company_rating": {
        "description": "Get quantitative financial health rating (A-F scale) based on DCF, ROE, ROA, D/E, P/E, P/B. Quick screening tool. Requires FMP_API_KEY (free).",
        "parameters": {
            "ticker": "Stock ticker symbol (e.g., 'AAPL')",
        },
    },
    "get_earnings_surprises": {
        "description": "Get historical earnings surprises (actual vs estimated EPS and revenue) with beat/miss rates. Strong signal for equity analysis. Requires FMP_API_KEY (free).",
        "parameters": {
            "ticker": "Stock ticker symbol (e.g., 'AAPL')",
            "limit": "Number of quarters (default: 8)",
        },
    },
}

FMP_TOOLS_BY_NAME: dict[str, Any] = {
    "get_analyst_estimates": get_analyst_estimates,
    "get_company_rating": get_company_rating,
    "get_earnings_surprises": get_earnings_surprises,
}
