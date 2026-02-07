"""
Yahoo Finance Tools for LangGraph.

All YFinance data fetching lives in this ONE file. This replaces three
separate implementations from v1:
    - yfinance_client.py      (async wrapper)
    - yfinance_metrics.py     (utility functions)
    - data_retrieval_agent.py (duplicate fetch methods, defined _fetch_historical_data TWICE)

Each function is decorated with @tool from langchain_core, making it
callable by the StepExecutorNode during DATA step execution.

Design decisions:
    - Tools are SYNCHRONOUS because yfinance itself is synchronous.
      LangGraph handles running them in an executor automatically.
    - Each tool returns a plain dict (JSON-serializable) -- no DataFrames
      in the return value, because the state must be serializable.
    - Error handling is inside each tool -- they return {"error": ...}
      instead of raising exceptions, so the graph can handle failures
      gracefully in the VerifierNode.
"""

import warnings
from datetime import datetime, timedelta
from typing import Any, Optional

import pandas as pd
import yfinance as yf
from langchain_core.tools import tool

# Suppress noisy yfinance warnings (e.g., FutureWarning from pandas)
warnings.filterwarnings("ignore", module="yfinance")


# =============================================================================
# Tool Registry
# =============================================================================
# This dict describes each tool's name, description, and parameters.
# The DecomposerNode uses this to tell the LLM what tools are available
# so it can generate correct tool_name and parameters in each step.
# =============================================================================

TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    "get_income_statements": {
        "description": "Get income statements (revenue, net income, etc.) for a company",
        "parameters": {
            "ticker": "Stock ticker symbol (e.g., 'AAPL')",
            "period": "'annual' or 'quarterly' (default: 'annual')",
            "limit": "Number of periods to return (default: 5)",
        },
    },
    "get_balance_sheets": {
        "description": "Get balance sheets (assets, liabilities, equity) for a company",
        "parameters": {
            "ticker": "Stock ticker symbol",
            "period": "'annual' or 'quarterly' (default: 'annual')",
            "limit": "Number of periods to return (default: 5)",
        },
    },
    "get_cash_flow_statements": {
        "description": "Get cash flow statements for a company",
        "parameters": {
            "ticker": "Stock ticker symbol",
            "period": "'annual' or 'quarterly' (default: 'annual')",
            "limit": "Number of periods to return (default: 5)",
        },
    },
    "get_current_stock_price": {
        "description": "Get current stock price, market cap, and basic market data",
        "parameters": {
            "ticker": "Stock ticker symbol",
        },
    },
    "get_historical_stock_prices": {
        "description": "Get historical daily stock prices for a date range",
        "parameters": {
            "ticker": "Stock ticker symbol",
            "start_date": "Start date in YYYY-MM-DD format",
            "end_date": "End date in YYYY-MM-DD format",
        },
    },
    "get_company_news": {
        "description": "Get recent news articles about a company",
        "parameters": {
            "ticker": "Stock ticker symbol",
            "limit": "Number of articles to return (default: 10)",
        },
    },
    "get_company_info": {
        "description": "Get basic company information (sector, industry, description, etc.)",
        "parameters": {
            "ticker": "Stock ticker symbol",
        },
    },
    "get_key_metrics": {
        "description": "Get key financial metrics (P/E ratio, margins, growth rates, etc.)",
        "parameters": {
            "ticker": "Stock ticker symbol",
        },
    },
    "get_analyst_recommendations": {
        "description": "Get Wall Street analyst Buy/Sell/Hold recommendations summary and recent rating changes",
        "parameters": {
            "ticker": "Stock ticker symbol",
        },
    },
    "get_institutional_holders": {
        "description": "Get top institutional holders (mutual funds, pension funds, etc.) and major holders breakdown",
        "parameters": {
            "ticker": "Stock ticker symbol",
        },
    },
    "get_options_overview": {
        "description": "Get options chain overview including put/call ratio, implied volatility, and available expiration dates. Useful as a sentiment indicator.",
        "parameters": {
            "ticker": "Stock ticker symbol",
        },
    },
}


def get_tool_descriptions_for_llm() -> str:
    """
    Format tool descriptions as a string for inclusion in LLM prompts.

    The DecomposerNode calls this to tell the LLM what tools are available,
    so it can generate correct step plans. Tools are grouped by data source
    for better LLM comprehension.

    Returns:
        A formatted string listing all tools with their descriptions and parameters.
    """
    # Group tools by source for clearer presentation
    groups = {
        "Yahoo Finance (no API key)": [
            "get_income_statements", "get_balance_sheets", "get_cash_flow_statements",
            "get_current_stock_price", "get_historical_stock_prices",
            "get_company_news", "get_company_info", "get_key_metrics",
            "get_analyst_recommendations", "get_institutional_holders", "get_options_overview",
        ],
        "Web Search (no API key)": [
            "web_search", "web_news_search",
        ],
        "SEC EDGAR (no API key)": [
            "get_sec_filings", "get_sec_financial_data", "get_insider_trades",
        ],
        "Federal Reserve / FRED (free API key)": [
            "get_economic_indicator", "get_treasury_yields",
        ],
        "Financial Modeling Prep / FMP (free tier API key)": [
            "get_analyst_estimates", "get_company_rating", "get_earnings_surprises",
        ],
    }

    lines = ["Available Financial Data Tools:\n"]

    for group_name, tool_names in groups.items():
        lines.append(f"--- {group_name} ---\n")
        for tool_name in tool_names:
            info = TOOL_REGISTRY.get(tool_name)
            if info is None:
                continue
            lines.append(f"  **{tool_name}**")
            lines.append(f"    Description: {info['description']}")
            if info.get("parameters"):
                lines.append("    Parameters:")
                for param_name, param_desc in info["parameters"].items():
                    lines.append(f"      - {param_name}: {param_desc}")
            else:
                lines.append("    Parameters: none")
            lines.append("")

    # Note any tools not in a group (future-proofing)
    grouped_tools = set()
    for names in groups.values():
        grouped_tools.update(names)
    ungrouped = [t for t in TOOL_REGISTRY if t not in grouped_tools]
    if ungrouped:
        lines.append("--- Other ---\n")
        for tool_name in ungrouped:
            info = TOOL_REGISTRY[tool_name]
            lines.append(f"  **{tool_name}**")
            lines.append(f"    Description: {info['description']}")
            if info.get("parameters"):
                lines.append("    Parameters:")
                for param_name, param_desc in info["parameters"].items():
                    lines.append(f"      - {param_name}: {param_desc}")
            lines.append("")

    return "\n".join(lines)


# =============================================================================
# Helper: Convert pandas Timestamps to strings
# =============================================================================

def _clean_for_json(data: Any) -> Any:
    """
    Recursively convert pandas Timestamps and other non-serializable types
    to strings so the result can be stored in LangGraph state.

    This is needed because yfinance returns DataFrames with Timestamp
    index/columns, and our state must be JSON-serializable.
    """
    if isinstance(data, dict):
        return {
            # Timestamp keys (e.g., column headers in financials) -> string
            (k.strftime("%Y-%m-%d") if hasattr(k, "strftime") else str(k)): _clean_for_json(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [_clean_for_json(item) for item in data]
    elif isinstance(data, pd.Timestamp):
        return data.strftime("%Y-%m-%d")
    elif isinstance(data, (pd.Series, pd.DataFrame)):
        return _clean_for_json(data.to_dict())
    elif pd.isna(data) if isinstance(data, (float, int)) else False:
        return None
    else:
        return data


# =============================================================================
# Tool Implementations
# =============================================================================
# Each @tool function:
#   1. Takes simple typed parameters
#   2. Calls yfinance synchronously
#   3. Returns a clean dict (no DataFrames, no Timestamps)
#   4. Catches exceptions and returns {"error": "..."} on failure
# =============================================================================


@tool
def get_income_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 5,
) -> dict[str, Any]:
    """Get income statements for a company using Yahoo Finance.

    Returns revenue, net income, gross profit, operating income, EBITDA,
    and other income statement line items for the specified number of periods.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
        period: 'annual' or 'quarterly'. Defaults to 'annual'.
        limit: Number of periods to return. Defaults to 5.
    """
    try:
        stock = yf.Ticker(ticker.upper())

        # yfinance has separate properties for annual vs quarterly
        if period.lower() == "quarterly":
            data = stock.quarterly_financials
        else:
            data = stock.financials

        # Handle empty data
        if data is None or data.empty:
            return {"error": f"No income statement data found for {ticker}"}

        # Limit columns (each column is a period) and convert to dict
        limited = data.iloc[:, :limit] if len(data.columns) > limit else data

        return {
            "ticker": ticker.upper(),
            "period": period,
            "data": _clean_for_json(limited.to_dict()),
        }

    except Exception as e:
        return {"error": f"Failed to fetch income statements for {ticker}: {str(e)}"}


@tool
def get_balance_sheets(
    ticker: str,
    period: str = "annual",
    limit: int = 5,
) -> dict[str, Any]:
    """Get balance sheets for a company using Yahoo Finance.

    Returns total assets, total liabilities, stockholders' equity,
    cash, debt, and other balance sheet line items.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
        period: 'annual' or 'quarterly'. Defaults to 'annual'.
        limit: Number of periods to return. Defaults to 5.
    """
    try:
        stock = yf.Ticker(ticker.upper())

        if period.lower() == "quarterly":
            data = stock.quarterly_balance_sheet
        else:
            data = stock.balance_sheet

        if data is None or data.empty:
            return {"error": f"No balance sheet data found for {ticker}"}

        limited = data.iloc[:, :limit] if len(data.columns) > limit else data

        return {
            "ticker": ticker.upper(),
            "period": period,
            "data": _clean_for_json(limited.to_dict()),
        }

    except Exception as e:
        return {"error": f"Failed to fetch balance sheets for {ticker}: {str(e)}"}


@tool
def get_cash_flow_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 5,
) -> dict[str, Any]:
    """Get cash flow statements for a company using Yahoo Finance.

    Returns operating cash flow, capital expenditures, free cash flow,
    and other cash flow statement items.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
        period: 'annual' or 'quarterly'. Defaults to 'annual'.
        limit: Number of periods to return. Defaults to 5.
    """
    try:
        stock = yf.Ticker(ticker.upper())

        if period.lower() == "quarterly":
            data = stock.quarterly_cashflow
        else:
            data = stock.cashflow

        if data is None or data.empty:
            return {"error": f"No cash flow data found for {ticker}"}

        limited = data.iloc[:, :limit] if len(data.columns) > limit else data

        return {
            "ticker": ticker.upper(),
            "period": period,
            "data": _clean_for_json(limited.to_dict()),
        }

    except Exception as e:
        return {"error": f"Failed to fetch cash flow for {ticker}: {str(e)}"}


@tool
def get_current_stock_price(ticker: str) -> dict[str, Any]:
    """Get current stock price and basic market data for a company.

    Returns current price, previous close, market cap, company name,
    currency, and last update timestamp.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        stock = yf.Ticker(ticker.upper())
        info = stock.info

        if not info:
            return {"error": f"No data found for ticker {ticker}"}

        # Get price from multiple possible fields (yfinance is inconsistent)
        current_price = (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or info.get("previousClose")
        )

        if current_price is None:
            return {"error": f"No price data available for {ticker}"}

        return {
            "ticker": ticker.upper(),
            "current_price": current_price,
            "previous_close": info.get("previousClose"),
            "open": info.get("open"),
            "day_low": info.get("dayLow"),
            "day_high": info.get("dayHigh"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
            "market_cap": info.get("marketCap"),
            "volume": info.get("volume"),
            "company_name": info.get("longName") or info.get("shortName"),
            "currency": info.get("currency", "USD"),
            "last_update": datetime.now().isoformat(),
        }

    except Exception as e:
        return {"error": f"Failed to fetch price for {ticker}: {str(e)}"}


@tool
def get_historical_stock_prices(
    ticker: str,
    start_date: str,
    end_date: str,
) -> dict[str, Any]:
    """Get historical daily stock prices for a date range.

    Returns daily open, high, low, close, volume data.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
    """
    try:
        stock = yf.Ticker(ticker.upper())
        data = stock.history(start=start_date, end=end_date)

        if data is None or data.empty:
            return {"error": f"No historical data found for {ticker} ({start_date} to {end_date})"}

        # Convert DataFrame to list of dicts with date as a field
        # (not as index) for clean JSON serialization
        records = []
        for date_idx, row in data.iterrows():
            record = {"date": date_idx.strftime("%Y-%m-%d")}
            record.update({k: v for k, v in row.items()})
            records.append(record)

        return {
            "ticker": ticker.upper(),
            "start_date": start_date,
            "end_date": end_date,
            "data_points": len(records),
            "data": records,
        }

    except Exception as e:
        return {"error": f"Failed to fetch history for {ticker}: {str(e)}"}


@tool
def get_company_news(ticker: str, limit: int = 10) -> dict[str, Any]:
    """Get recent news articles about a company.

    Returns news headlines, publishers, links, and publication dates.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
        limit: Maximum number of articles to return. Defaults to 10.
    """
    try:
        stock = yf.Ticker(ticker.upper())
        news = stock.news

        if not news:
            return {"error": f"No news found for {ticker}"}

        # Limit and return
        limited_news = news[:limit] if len(news) > limit else news

        return {
            "ticker": ticker.upper(),
            "article_count": len(limited_news),
            "news": limited_news,
        }

    except Exception as e:
        return {"error": f"Failed to fetch news for {ticker}: {str(e)}"}


@tool
def get_company_info(ticker: str) -> dict[str, Any]:
    """Get basic company information including sector, industry, and description.

    Returns company name, sector, industry, website, employee count,
    business summary, and market cap.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        stock = yf.Ticker(ticker.upper())
        info = stock.info

        if not info:
            return {"error": f"No company info found for {ticker}"}

        return {
            "ticker": ticker.upper(),
            "company_name": info.get("longName") or info.get("shortName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "website": info.get("website"),
            "summary": info.get("longBusinessSummary"),
            "employees": info.get("fullTimeEmployees"),
            "market_cap": info.get("marketCap"),
            "currency": info.get("currency", "USD"),
            "country": info.get("country"),
            "exchange": info.get("exchange"),
        }

    except Exception as e:
        return {"error": f"Failed to fetch company info for {ticker}: {str(e)}"}


@tool
def get_key_metrics(ticker: str) -> dict[str, Any]:
    """Get key financial metrics for a company.

    Returns valuation ratios (P/E, P/B, P/S), profitability metrics
    (margins, ROE, ROA), growth metrics, dividend info, and risk metrics.

    This is a comprehensive "snapshot" tool -- use it when the user wants
    an overview of a company's financial health.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        stock = yf.Ticker(ticker.upper())
        info = stock.info

        if not info:
            return {"error": f"No metrics data found for {ticker}"}

        return {
            "ticker": ticker.upper(),
            "company_name": info.get("longName") or info.get("shortName"),

            # --- Valuation ---
            "trailing_pe": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "peg_ratio": info.get("trailingPegRatio"),
            "price_to_book": info.get("priceToBook"),
            "price_to_sales": info.get("priceToSalesTrailing12Months"),
            "enterprise_value": info.get("enterpriseValue"),
            "ev_to_revenue": info.get("enterpriseToRevenue"),
            "ev_to_ebitda": info.get("enterpriseToEbitda"),

            # --- Profitability ---
            "profit_margins": info.get("profitMargins"),
            "gross_margins": info.get("grossMargins"),
            "operating_margins": info.get("operatingMargins"),
            "ebitda_margins": info.get("ebitdaMargins"),
            "return_on_equity": info.get("returnOnEquity"),
            "return_on_assets": info.get("returnOnAssets"),

            # --- Growth ---
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
            "earnings_quarterly_growth": info.get("earningsQuarterlyGrowth"),

            # --- Income ---
            "total_revenue": info.get("totalRevenue"),
            "revenue_per_share": info.get("revenuePerShare"),
            "trailing_eps": info.get("trailingEps"),
            "forward_eps": info.get("forwardEps"),
            "ebitda": info.get("ebitda"),
            "free_cashflow": info.get("freeCashflow"),

            # --- Balance Sheet ---
            "total_cash": info.get("totalCash"),
            "total_debt": info.get("totalDebt"),
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "quick_ratio": info.get("quickRatio"),
            "book_value": info.get("bookValue"),

            # --- Dividends ---
            "dividend_yield": info.get("dividendYield"),
            "dividend_rate": info.get("dividendRate"),
            "payout_ratio": info.get("payoutRatio"),

            # --- Risk ---
            "beta": info.get("beta"),
            "short_ratio": info.get("shortRatio"),

            # --- Market ---
            "market_cap": info.get("marketCap"),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
        }

    except Exception as e:
        return {"error": f"Failed to fetch key metrics for {ticker}: {str(e)}"}


# =============================================================================
# Additional YFinance Tools
# =============================================================================
# These leverage yfinance properties that weren't exposed in the original
# tool set but are valuable for equity analysis.
# =============================================================================


@tool
def get_analyst_recommendations(ticker: str) -> dict[str, Any]:
    """Get Wall Street analyst recommendations for a company.

    Returns a summary of Buy/Sell/Hold ratings and recent individual
    analyst rating changes (upgrades and downgrades).

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        stock = yf.Ticker(ticker.upper())

        result: dict[str, Any] = {"ticker": ticker.upper()}

        # --- Recommendations summary (aggregated) ---
        try:
            rec_summary = stock.recommendations_summary
            if rec_summary is not None and not rec_summary.empty:
                summary_records = []
                for _, row in rec_summary.iterrows():
                    summary_records.append({
                        k: (int(v) if isinstance(v, (int, float)) and not pd.isna(v) else v)
                        for k, v in row.items()
                    })
                result["recommendations_summary"] = summary_records
        except Exception:
            result["recommendations_summary"] = []

        # --- Recent individual analyst actions ---
        try:
            recs = stock.recommendations
            if recs is not None and not recs.empty:
                recent = recs.tail(15)  # Last 15 actions
                rec_records = []
                for date_idx, row in recent.iterrows():
                    record = {
                        "date": date_idx.strftime("%Y-%m-%d") if hasattr(date_idx, "strftime") else str(date_idx),
                    }
                    record.update({k: v for k, v in row.items() if not pd.isna(v)})
                    rec_records.append(record)
                rec_records.reverse()  # Most recent first
                result["recent_actions"] = rec_records
        except Exception:
            result["recent_actions"] = []

        if not result.get("recommendations_summary") and not result.get("recent_actions"):
            return {"error": f"No analyst recommendation data found for {ticker}"}

        return result

    except Exception as e:
        return {"error": f"Failed to fetch analyst recommendations for {ticker}: {str(e)}"}


@tool
def get_institutional_holders(ticker: str) -> dict[str, Any]:
    """Get institutional ownership data for a company.

    Returns top institutional holders (mutual funds, pension funds, hedge
    funds) and a breakdown of insider vs. institutional ownership.

    High institutional ownership often indicates a well-researched stock.
    Changes in institutional holdings can signal smart money moves.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        stock = yf.Ticker(ticker.upper())

        result: dict[str, Any] = {"ticker": ticker.upper()}

        # --- Major holders breakdown ---
        try:
            major = stock.major_holders
            if major is not None and not major.empty:
                holders_dict = {}
                for _, row in major.iterrows():
                    # major_holders has columns [0, 1] -> value, description
                    val = row.iloc[0] if len(row) > 0 else ""
                    desc = row.iloc[1] if len(row) > 1 else ""
                    holders_dict[str(desc)] = str(val)
                result["ownership_breakdown"] = holders_dict
        except Exception:
            result["ownership_breakdown"] = {}

        # --- Top institutional holders ---
        try:
            inst = stock.institutional_holders
            if inst is not None and not inst.empty:
                holders = []
                for _, row in inst.head(15).iterrows():
                    holder = {}
                    for col in inst.columns:
                        val = row[col]
                        if hasattr(val, "strftime"):
                            holder[col] = val.strftime("%Y-%m-%d")
                        elif isinstance(val, (int, float)) and not pd.isna(val):
                            holder[col] = val
                        elif pd.isna(val):
                            holder[col] = None
                        else:
                            holder[col] = str(val)
                    holders.append(holder)
                result["top_institutional_holders"] = holders
        except Exception:
            result["top_institutional_holders"] = []

        if not result.get("ownership_breakdown") and not result.get("top_institutional_holders"):
            return {"error": f"No institutional holder data found for {ticker}"}

        return result

    except Exception as e:
        return {"error": f"Failed to fetch institutional holders for {ticker}: {str(e)}"}


@tool
def get_options_overview(ticker: str) -> dict[str, Any]:
    """Get options market overview for a company.

    Returns available expiration dates, and for the nearest expiration:
    put/call volume ratio, open interest, and implied volatility.
    The put/call ratio is a widely used sentiment indicator:
    - High ratio (>1) = bearish sentiment
    - Low ratio (<0.7) = bullish sentiment

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        stock = yf.Ticker(ticker.upper())

        # Get available expiration dates
        try:
            expirations = stock.options
        except Exception:
            return {"error": f"No options data available for {ticker}"}

        if not expirations:
            return {"error": f"No options expiration dates found for {ticker}"}

        result: dict[str, Any] = {
            "ticker": ticker.upper(),
            "expiration_dates": list(expirations[:10]),  # First 10
            "total_expirations": len(expirations),
        }

        # Get nearest expiration chain for sentiment analysis
        nearest_exp = expirations[0]
        try:
            chain = stock.option_chain(nearest_exp)
            calls = chain.calls
            puts = chain.puts

            # Aggregate volume and open interest
            call_volume = int(calls["volume"].sum()) if "volume" in calls.columns else 0
            put_volume = int(puts["volume"].sum()) if "volume" in puts.columns else 0
            call_oi = int(calls["openInterest"].sum()) if "openInterest" in calls.columns else 0
            put_oi = int(puts["openInterest"].sum()) if "openInterest" in puts.columns else 0

            # Put/Call ratios
            pc_volume_ratio = round(put_volume / call_volume, 3) if call_volume > 0 else None
            pc_oi_ratio = round(put_oi / call_oi, 3) if call_oi > 0 else None

            # Average implied volatility
            call_iv = round(float(calls["impliedVolatility"].mean()), 4) if "impliedVolatility" in calls.columns else None
            put_iv = round(float(puts["impliedVolatility"].mean()), 4) if "impliedVolatility" in puts.columns else None

            # Sentiment interpretation
            sentiment = "NEUTRAL"
            if pc_volume_ratio is not None:
                if pc_volume_ratio > 1.0:
                    sentiment = "BEARISH (high put activity)"
                elif pc_volume_ratio < 0.7:
                    sentiment = "BULLISH (high call activity)"

            result["nearest_expiration"] = {
                "date": nearest_exp,
                "call_volume": call_volume,
                "put_volume": put_volume,
                "call_open_interest": call_oi,
                "put_open_interest": put_oi,
                "put_call_volume_ratio": pc_volume_ratio,
                "put_call_oi_ratio": pc_oi_ratio,
                "avg_call_implied_volatility": call_iv,
                "avg_put_implied_volatility": put_iv,
                "sentiment_signal": sentiment,
            }

        except Exception as e:
            result["nearest_expiration"] = {"error": f"Could not fetch chain: {str(e)}"}

        return result

    except Exception as e:
        return {"error": f"Failed to fetch options data for {ticker}: {str(e)}"}


# =============================================================================
# Tool Lookup
# =============================================================================
# The StepExecutorNode uses this to find and call the right tool by name.
# ALL tools from ALL sources are merged into TOOLS_BY_NAME and TOOL_REGISTRY
# so the executor has a single lookup point.
# =============================================================================

# Map of tool_name -> callable tool function
TOOLS_BY_NAME: dict[str, Any] = {
    # --- YFinance tools ---
    "get_income_statements": get_income_statements,
    "get_balance_sheets": get_balance_sheets,
    "get_cash_flow_statements": get_cash_flow_statements,
    "get_current_stock_price": get_current_stock_price,
    "get_historical_stock_prices": get_historical_stock_prices,
    "get_company_news": get_company_news,
    "get_company_info": get_company_info,
    "get_key_metrics": get_key_metrics,
    "get_analyst_recommendations": get_analyst_recommendations,
    "get_institutional_holders": get_institutional_holders,
    "get_options_overview": get_options_overview,
}

# --- Merge in web search tools ---
from src.tools.web_search import WEB_TOOLS_BY_NAME, WEB_TOOL_REGISTRY

TOOLS_BY_NAME.update(WEB_TOOLS_BY_NAME)
TOOL_REGISTRY.update(WEB_TOOL_REGISTRY)

# --- Merge in SEC EDGAR tools ---
from src.tools.sec_edgar_tools import SEC_TOOLS_BY_NAME, SEC_TOOL_REGISTRY

TOOLS_BY_NAME.update(SEC_TOOLS_BY_NAME)
TOOL_REGISTRY.update(SEC_TOOL_REGISTRY)

# --- Merge in FRED tools ---
from src.tools.fred_tools import FRED_TOOLS_BY_NAME, FRED_TOOL_REGISTRY

TOOLS_BY_NAME.update(FRED_TOOLS_BY_NAME)
TOOL_REGISTRY.update(FRED_TOOL_REGISTRY)

# --- Merge in FMP tools ---
from src.tools.fmp_tools import FMP_TOOLS_BY_NAME, FMP_TOOL_REGISTRY

TOOLS_BY_NAME.update(FMP_TOOLS_BY_NAME)
TOOL_REGISTRY.update(FMP_TOOL_REGISTRY)

# List of all tool objects (for passing to LLM bind_tools if needed)
ALL_TOOLS = list(TOOLS_BY_NAME.values())
