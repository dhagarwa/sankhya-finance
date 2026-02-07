"""
FRED (Federal Reserve Economic Data) Tools for LangGraph.

Provides access to the FRED API for macroeconomic indicators. This is
essential for equity analysis because stock valuations don't exist in a
vacuum -- interest rates, inflation, GDP growth, and unemployment all
drive sector rotations, multiples, and earnings expectations.

Requires: FRED_API_KEY (free -- register at https://fred.stlouisfed.org/docs/api/api_key.html)

If the API key is not set, tools return a helpful error message with
the registration URL instead of crashing.
"""

import os
from datetime import datetime, timedelta
from typing import Any

import requests
from langchain_core.tools import tool


# =============================================================================
# Configuration
# =============================================================================

FRED_BASE = "https://api.stlouisfed.org/fred"


def _get_fred_key() -> str | None:
    """Get FRED API key from environment."""
    return os.getenv("FRED_API_KEY")


def _fred_get(endpoint: str, params: dict) -> dict:
    """Make a request to the FRED API."""
    api_key = _get_fred_key()
    if not api_key:
        raise EnvironmentError(
            "FRED_API_KEY not set. Get a free key at: "
            "https://fred.stlouisfed.org/docs/api/api_key.html  "
            "Then add FRED_API_KEY=your-key to your .env file."
        )

    params["api_key"] = api_key
    params["file_type"] = "json"

    resp = requests.get(f"{FRED_BASE}/{endpoint}", params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


# =============================================================================
# Common Economic Indicators (friendly name -> FRED series ID)
# =============================================================================

COMMON_INDICATORS: dict[str, dict[str, str]] = {
    # GDP & Growth
    "gdp": {"series_id": "GDP", "description": "Gross Domestic Product (nominal, quarterly, billions USD)"},
    "real_gdp": {"series_id": "GDPC1", "description": "Real GDP (inflation-adjusted, quarterly, billions USD)"},
    "gdp_growth": {"series_id": "A191RL1Q225SBEA", "description": "Real GDP Growth Rate (quarterly, %)"},

    # Inflation
    "cpi": {"series_id": "CPIAUCSL", "description": "Consumer Price Index (monthly)"},
    "core_cpi": {"series_id": "CPILFESL", "description": "Core CPI excl. Food & Energy (monthly)"},
    "pce": {"series_id": "PCEPI", "description": "Personal Consumption Expenditure Price Index (monthly)"},

    # Employment
    "unemployment": {"series_id": "UNRATE", "description": "Unemployment Rate (monthly, %)"},
    "nonfarm_payrolls": {"series_id": "PAYEMS", "description": "Total Nonfarm Payrolls (monthly, thousands)"},
    "initial_claims": {"series_id": "ICSA", "description": "Initial Jobless Claims (weekly)"},

    # Interest Rates
    "fed_funds_rate": {"series_id": "FEDFUNDS", "description": "Federal Funds Effective Rate (monthly, %)"},
    "fed_funds_daily": {"series_id": "DFF", "description": "Federal Funds Rate (daily, %)"},
    "prime_rate": {"series_id": "DPRIME", "description": "Bank Prime Loan Rate (daily, %)"},

    # Treasury Yields
    "treasury_3m": {"series_id": "DGS3MO", "description": "3-Month Treasury Yield (daily, %)"},
    "treasury_2y": {"series_id": "DGS2", "description": "2-Year Treasury Yield (daily, %)"},
    "treasury_5y": {"series_id": "DGS5", "description": "5-Year Treasury Yield (daily, %)"},
    "treasury_10y": {"series_id": "DGS10", "description": "10-Year Treasury Yield (daily, %)"},
    "treasury_30y": {"series_id": "DGS30", "description": "30-Year Treasury Yield (daily, %)"},

    # Market Indicators
    "sp500": {"series_id": "SP500", "description": "S&P 500 Index (daily)"},
    "vix": {"series_id": "VIXCLS", "description": "CBOE Volatility Index - VIX (daily)"},

    # Housing
    "housing_starts": {"series_id": "HOUST", "description": "Housing Starts (monthly, thousands)"},
    "case_shiller": {"series_id": "CSUSHPISA", "description": "S&P/Case-Shiller Home Price Index (monthly)"},

    # Consumer & Business
    "consumer_sentiment": {"series_id": "UMCSENT", "description": "University of Michigan Consumer Sentiment (monthly)"},
    "retail_sales": {"series_id": "RSAFS", "description": "Advance Retail Sales (monthly, millions USD)"},
    "industrial_production": {"series_id": "INDPRO", "description": "Industrial Production Index (monthly)"},

    # Money Supply
    "m2": {"series_id": "M2SL", "description": "M2 Money Stock (monthly, billions USD)"},

    # Corporate
    "corporate_bond_yield": {"series_id": "BAMLC0A4CBBBEY", "description": "ICE BofA BBB US Corporate Bond Yield (daily, %)"},
    "high_yield_spread": {"series_id": "BAMLH0A0HYM2EY", "description": "ICE BofA US High Yield Spread (daily, %)"},
}


# =============================================================================
# Tool Implementations
# =============================================================================


@tool
def get_economic_indicator(
    indicator: str,
    start_date: str = "",
    end_date: str = "",
    limit: int = 60,
) -> dict[str, Any]:
    """Get macroeconomic data from the Federal Reserve (FRED).

    Essential for equity analysis context: interest rates drive valuations,
    inflation affects margins, GDP growth drives revenue expectations.

    Use friendly names like 'fed_funds_rate', 'unemployment', 'cpi',
    'gdp_growth', etc. Or pass a raw FRED series ID directly.

    Args:
        indicator: Friendly name (e.g., 'fed_funds_rate', 'treasury_10y', 'unemployment',
            'cpi', 'gdp_growth', 'sp500', 'vix') OR a raw FRED series ID (e.g., 'DGS10').
            Call with indicator='LIST' to see all available friendly names.
        start_date: Start date in YYYY-MM-DD format (default: 5 years ago).
        end_date: End date in YYYY-MM-DD format (default: today).
        limit: Maximum number of observations (default: 60, most recent).
    """
    try:
        # Special case: list all available indicators
        if indicator.upper() == "LIST":
            return {
                "available_indicators": {
                    name: info["description"]
                    for name, info in COMMON_INDICATORS.items()
                },
                "note": "Pass any of these names as the 'indicator' parameter, "
                        "or use a raw FRED series ID directly.",
            }

        # Resolve friendly name to series ID
        indicator_lower = indicator.lower().strip()
        if indicator_lower in COMMON_INDICATORS:
            series_id = COMMON_INDICATORS[indicator_lower]["series_id"]
            description = COMMON_INDICATORS[indicator_lower]["description"]
        else:
            # Assume it's a raw FRED series ID
            series_id = indicator.upper().strip()
            description = f"FRED series: {series_id}"

        # Default date range
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")

        # Fetch data
        params = {
            "series_id": series_id,
            "observation_start": start_date,
            "observation_end": end_date,
            "sort_order": "desc",
            "limit": limit,
        }
        data = _fred_get("series/observations", params)

        # Also get series info
        series_info = _fred_get("series", {"series_id": series_id})
        series_meta = series_info.get("seriess", [{}])[0]

        # Clean observations
        observations = []
        for obs in data.get("observations", []):
            val = obs.get("value", ".")
            if val == ".":
                continue  # Missing data point
            try:
                numeric_val = float(val)
            except (ValueError, TypeError):
                numeric_val = val

            observations.append({
                "date": obs.get("date", ""),
                "value": numeric_val,
            })

        # Compute basic stats from the data
        numeric_values = [o["value"] for o in observations if isinstance(o["value"], (int, float))]
        stats = {}
        if numeric_values:
            stats = {
                "latest_value": numeric_values[0],
                "latest_date": observations[0]["date"] if observations else "",
                "min": min(numeric_values),
                "max": max(numeric_values),
                "average": round(sum(numeric_values) / len(numeric_values), 4),
            }
            if len(numeric_values) >= 2:
                stats["change_from_previous"] = round(numeric_values[0] - numeric_values[1], 4)

        return {
            "indicator": indicator_lower if indicator_lower in COMMON_INDICATORS else series_id,
            "series_id": series_id,
            "description": description,
            "frequency": series_meta.get("frequency", ""),
            "units": series_meta.get("units", ""),
            "seasonal_adjustment": series_meta.get("seasonal_adjustment", ""),
            "last_updated": series_meta.get("last_updated", ""),
            "observation_count": len(observations),
            "statistics": stats,
            "observations": observations,
        }

    except EnvironmentError as e:
        return {"error": str(e)}
    except requests.exceptions.HTTPError as e:
        return {"error": f"FRED API error for '{indicator}': {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to fetch FRED data for '{indicator}': {str(e)}"}


@tool
def get_treasury_yields() -> dict[str, Any]:
    """Get the current US Treasury yield curve (3M, 2Y, 5Y, 10Y, 30Y).

    The yield curve is critical for equity analysis:
    - An inverted curve (2Y > 10Y) historically signals recession
    - Rising long-term yields pressure growth stock valuations
    - The spread between corporate bonds and treasuries indicates credit risk

    Returns the latest yield for each maturity plus the 2Y-10Y spread.
    No parameters needed -- returns the most recent data.
    """
    try:
        maturities = {
            "3_month": "DGS3MO",
            "2_year": "DGS2",
            "5_year": "DGS5",
            "10_year": "DGS10",
            "30_year": "DGS30",
        }

        api_key = _get_fred_key()
        if not api_key:
            return {
                "error": "FRED_API_KEY not set. Get a free key at: "
                         "https://fred.stlouisfed.org/docs/api/api_key.html  "
                         "Then add FRED_API_KEY=your-key to your .env file."
            }

        yields_data = {}
        for name, series_id in maturities.items():
            params = {
                "series_id": series_id,
                "sort_order": "desc",
                "limit": 5,  # Get a few in case latest is missing
            }
            data = _fred_get("series/observations", params)

            for obs in data.get("observations", []):
                val = obs.get("value", ".")
                if val != ".":
                    yields_data[name] = {
                        "yield_pct": float(val),
                        "date": obs["date"],
                    }
                    break

        # Calculate key spreads
        spreads = {}
        if "2_year" in yields_data and "10_year" in yields_data:
            spread_2_10 = round(
                yields_data["10_year"]["yield_pct"] - yields_data["2_year"]["yield_pct"],
                3,
            )
            spreads["2y_10y_spread"] = spread_2_10
            spreads["yield_curve_status"] = (
                "INVERTED (recession signal)" if spread_2_10 < 0
                else "FLAT (caution)" if spread_2_10 < 0.25
                else "NORMAL"
            )

        if "3_month" in yields_data and "10_year" in yields_data:
            spreads["3m_10y_spread"] = round(
                yields_data["10_year"]["yield_pct"] - yields_data["3_month"]["yield_pct"],
                3,
            )

        return {
            "data_source": "Federal Reserve (FRED)",
            "yields": yields_data,
            "spreads": spreads,
            "note": "Yields are in percent (%). A negative 2Y-10Y spread "
                    "indicates yield curve inversion, historically a recession predictor.",
        }

    except EnvironmentError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Failed to fetch treasury yields: {str(e)}"}


# =============================================================================
# Tool Registry (for the Decomposer to describe to the LLM)
# =============================================================================

FRED_TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    "get_economic_indicator": {
        "description": "Get macroeconomic data from FRED (Federal Reserve). Supports: fed_funds_rate, treasury_10y, unemployment, cpi, gdp_growth, sp500, vix, and 25+ more indicators. Essential for macro context in equity analysis. Requires FRED_API_KEY (free).",
        "parameters": {
            "indicator": "Friendly name (e.g., 'fed_funds_rate', 'treasury_10y', 'unemployment', 'cpi', 'gdp_growth', 'sp500', 'vix') or raw FRED series ID. Use 'LIST' to see all available.",
            "start_date": "Start date YYYY-MM-DD (default: 5 years ago)",
            "end_date": "End date YYYY-MM-DD (default: today)",
            "limit": "Max observations to return (default: 60)",
        },
    },
    "get_treasury_yields": {
        "description": "Get current US Treasury yield curve (3M through 30Y) with 2Y-10Y spread and inversion status. Critical for valuation context. Requires FRED_API_KEY (free).",
        "parameters": {},
    },
}

FRED_TOOLS_BY_NAME: dict[str, Any] = {
    "get_economic_indicator": get_economic_indicator,
    "get_treasury_yields": get_treasury_yields,
}
