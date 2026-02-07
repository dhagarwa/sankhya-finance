"""
SEC EDGAR Tools for LangGraph.

Provides access to SEC EDGAR public APIs -- completely free, no API key.
SEC only requires a descriptive User-Agent header with contact info.

What this adds over YFinance:
    - Official SEC filings list (10-K, 10-Q, 8-K, proxy, etc.)
    - Structured XBRL financial data directly from filings (more reliable
      than YFinance for historical fundamentals)
    - Insider transactions reported to the SEC (Forms 3, 4, 5)

SEC EDGAR rate limit: 10 requests/second.
"""

import os
import time
from datetime import datetime
from functools import lru_cache
from typing import Any

import requests
from langchain_core.tools import tool


# =============================================================================
# Configuration
# =============================================================================

SEC_HEADERS = {
    "User-Agent": os.getenv(
        "SEC_USER_AGENT",
        "SankhyaFinance research@sankhya.finance"
    ),
    "Accept-Encoding": "gzip, deflate",
}

SEC_BASE = "https://data.sec.gov"

# Rate limiting: SEC allows 10 req/s, we'll be conservative
_last_request_time = 0.0


def _sec_get(url: str) -> requests.Response:
    """Make a rate-limited GET request to SEC EDGAR."""
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < 0.12:  # ~8 req/s max to stay safe
        time.sleep(0.12 - elapsed)

    resp = requests.get(url, headers=SEC_HEADERS, timeout=15)
    _last_request_time = time.time()
    resp.raise_for_status()
    return resp


# =============================================================================
# Ticker -> CIK Mapping
# =============================================================================

@lru_cache(maxsize=1)
def _get_ticker_to_cik_map() -> dict[str, int]:
    """
    Fetch and cache the SEC ticker-to-CIK mapping.

    SEC publishes this at a well-known URL. We cache it in memory
    for the lifetime of the process (~1 query session).
    """
    url = "https://www.sec.gov/files/company_tickers.json"
    resp = _sec_get(url)
    data = resp.json()
    return {
        entry["ticker"].upper(): int(entry["cik_str"])
        for entry in data.values()
    }


def _ticker_to_cik(ticker: str) -> int | None:
    """Convert a stock ticker to SEC CIK number."""
    try:
        mapping = _get_ticker_to_cik_map()
        return mapping.get(ticker.upper())
    except Exception:
        return None


def _pad_cik(cik: int) -> str:
    """Pad CIK to 10 digits as SEC requires."""
    return str(cik).zfill(10)


# =============================================================================
# Tool Implementations
# =============================================================================


@tool
def get_sec_filings(
    ticker: str,
    filing_type: str = "10-K",
    limit: int = 10,
) -> dict[str, Any]:
    """Get recent SEC filings for a company from the EDGAR database.

    Returns filing metadata including date, type, description, and URL
    for each filing. Use filing_type to filter (e.g., '10-K' for annual
    reports, '10-Q' for quarterly, '8-K' for current reports).

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
        filing_type: SEC form type to filter by (default: '10-K').
            Common types: '10-K', '10-Q', '8-K', 'DEF 14A', 'S-1', '4'.
            Use 'ALL' to get all filing types.
        limit: Maximum number of filings to return (default: 10).
    """
    try:
        cik = _ticker_to_cik(ticker)
        if cik is None:
            return {"error": f"Could not find SEC CIK for ticker '{ticker}'"}

        padded_cik = _pad_cik(cik)
        url = f"{SEC_BASE}/submissions/CIK{padded_cik}.json"
        resp = _sec_get(url)
        data = resp.json()

        # Extract recent filings
        recent = data.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        dates = recent.get("filingDate", [])
        accessions = recent.get("accessionNumber", [])
        primary_docs = recent.get("primaryDocument", [])
        descriptions = recent.get("primaryDocDescription", [])

        filings = []
        for i in range(len(forms)):
            form = forms[i] if i < len(forms) else ""
            # Filter by type unless 'ALL'
            if filing_type.upper() != "ALL" and form != filing_type:
                continue

            accession = accessions[i].replace("-", "") if i < len(accessions) else ""
            primary_doc = primary_docs[i] if i < len(primary_docs) else ""
            filing_url = (
                f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{primary_doc}"
                if accession and primary_doc else ""
            )

            filings.append({
                "form_type": form,
                "filing_date": dates[i] if i < len(dates) else "",
                "description": descriptions[i] if i < len(descriptions) else "",
                "accession_number": accessions[i] if i < len(accessions) else "",
                "url": filing_url,
            })

            if len(filings) >= limit:
                break

        return {
            "ticker": ticker.upper(),
            "company_name": data.get("name", ""),
            "cik": str(cik),
            "filing_type_filter": filing_type,
            "filing_count": len(filings),
            "filings": filings,
        }

    except requests.exceptions.HTTPError as e:
        return {"error": f"SEC EDGAR HTTP error for {ticker}: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to fetch SEC filings for {ticker}: {str(e)}"}


@tool
def get_sec_financial_data(
    ticker: str,
    metrics: str = "revenue,net_income,eps,total_assets,total_liabilities",
) -> dict[str, Any]:
    """Get structured financial data from SEC XBRL filings.

    Returns historical financial metrics directly from SEC filings
    (more authoritative than Yahoo Finance for fundamental data).
    Data is extracted from companies' XBRL-tagged 10-K and 10-Q filings.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
        metrics: Comma-separated list of metrics to retrieve. Available:
            revenue, net_income, eps, eps_diluted, gross_profit,
            operating_income, total_assets, total_liabilities,
            stockholders_equity, cash, long_term_debt, shares_outstanding,
            operating_cash_flow, capex.
    """
    try:
        cik = _ticker_to_cik(ticker)
        if cik is None:
            return {"error": f"Could not find SEC CIK for ticker '{ticker}'"}

        padded_cik = _pad_cik(cik)
        url = f"{SEC_BASE}/api/xbrl/companyfacts/CIK{padded_cik}.json"
        resp = _sec_get(url)
        data = resp.json()

        facts = data.get("facts", {})

        # Support both US-GAAP (domestic filers) and IFRS (foreign filers like TSM, ASML, NVO)
        us_gaap = facts.get("us-gaap", {})
        ifrs_full = facts.get("ifrs-full", {})
        accounting_standard = "us-gaap" if us_gaap else ("ifrs" if ifrs_full else "unknown")

        # Map friendly names to XBRL concept names.
        # Each entry lists concepts to try in order; we search BOTH namespaces.
        # US-GAAP concepts listed first, then IFRS equivalents.
        metric_mapping: dict[str, list[tuple[str, dict]]] = {
            "revenue": [
                # (concept_name, namespace_dict)
                *[(c, us_gaap) for c in [
                    "Revenues",
                    "RevenueFromContractWithCustomerExcludingAssessedTax",
                    "SalesRevenueNet",
                    "RevenueFromContractWithCustomerIncludingAssessedTax",
                ]],
                *[(c, ifrs_full) for c in [
                    "Revenue",
                    "RevenueFromContractsWithCustomers",
                ]],
            ],
            "net_income": [
                *[(c, us_gaap) for c in ["NetIncomeLoss"]],
                *[(c, ifrs_full) for c in [
                    "ProfitLoss",
                    "ProfitLossAttributableToOwnersOfParent",
                ]],
            ],
            "eps": [
                *[(c, us_gaap) for c in ["EarningsPerShareBasic"]],
                *[(c, ifrs_full) for c in ["BasicEarningsLossPerShare"]],
            ],
            "eps_diluted": [
                *[(c, us_gaap) for c in ["EarningsPerShareDiluted"]],
                *[(c, ifrs_full) for c in ["DilutedEarningsLossPerShare"]],
            ],
            "gross_profit": [
                *[(c, us_gaap) for c in ["GrossProfit"]],
                *[(c, ifrs_full) for c in ["GrossProfit"]],
            ],
            "operating_income": [
                *[(c, us_gaap) for c in ["OperatingIncomeLoss"]],
                *[(c, ifrs_full) for c in ["ProfitLossFromOperatingActivities"]],
            ],
            "total_assets": [
                *[(c, us_gaap) for c in ["Assets"]],
                *[(c, ifrs_full) for c in ["Assets"]],
            ],
            "total_liabilities": [
                *[(c, us_gaap) for c in ["Liabilities"]],
                *[(c, ifrs_full) for c in ["Liabilities"]],
            ],
            "stockholders_equity": [
                *[(c, us_gaap) for c in [
                    "StockholdersEquity",
                    "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
                ]],
                *[(c, ifrs_full) for c in [
                    "Equity",
                    "EquityAttributableToOwnersOfParent",
                ]],
            ],
            "cash": [
                *[(c, us_gaap) for c in [
                    "CashAndCashEquivalentsAtCarryingValue",
                    "CashCashEquivalentsAndShortTermInvestments",
                ]],
                *[(c, ifrs_full) for c in ["CashAndCashEquivalents"]],
            ],
            "long_term_debt": [
                *[(c, us_gaap) for c in ["LongTermDebt", "LongTermDebtNoncurrent"]],
                *[(c, ifrs_full) for c in ["NoncurrentFinancialLiabilities", "NoncurrentLiabilities"]],
            ],
            "shares_outstanding": [
                *[(c, us_gaap) for c in [
                    "CommonStockSharesOutstanding",
                    "WeightedAverageNumberOfShareOutstandingBasicAndDiluted",
                ]],
                *[(c, ifrs_full) for c in [
                    "WeightedAverageShares",
                ]],
            ],
            "operating_cash_flow": [
                *[(c, us_gaap) for c in [
                    "NetCashProvidedByUsedInOperatingActivities",
                    "NetCashProvidedByOperatingActivities",
                    "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
                ]],
                *[(c, ifrs_full) for c in [
                    "CashFlowsFromUsedInOperatingActivities",
                ]],
            ],
            "capex": [
                *[(c, us_gaap) for c in [
                    "PaymentsToAcquirePropertyPlantAndEquipment",
                    "PaymentsForCapitalImprovements",
                ]],
                *[(c, ifrs_full) for c in [
                    "PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities",
                ]],
            ],
        }

        # Determine which annual filing forms to look for.
        # US companies use 10-K; foreign private issuers use 20-F or 40-F.
        annual_forms = {"10-K", "20-F", "40-F"}
        quarterly_forms = {"10-Q", "6-K"}  # 6-K is the foreign equivalent of 10-Q/8-K

        requested = [m.strip().lower() for m in metrics.split(",")]
        results = {}

        for metric_name in requested:
            if metric_name not in metric_mapping:
                results[metric_name] = {"error": f"Unknown metric '{metric_name}'"}
                continue

            # Try each possible XBRL concept -- pick the one with the MOST RECENT data.
            concept_data = None
            used_concept = None
            best_max_year = 0
            best_count = 0
            for concept, namespace in metric_mapping[metric_name]:
                if not namespace or concept not in namespace:
                    continue
                candidate = namespace[concept]
                units = candidate.get("units", {})
                values = units.get("USD") or units.get("USD/shares") or units.get("shares") or units.get("TWD") or []
                annual_entries = [
                    v for v in values
                    if (v.get("form") or "") in annual_forms and (v.get("fp") or "") == "FY"
                ]
                if not annual_entries:
                    continue
                max_year = max(v.get("fy", 0) for v in annual_entries)
                count = len(annual_entries)
                if max_year > best_max_year or (max_year == best_max_year and count > best_count):
                    best_max_year = max_year
                    best_count = count
                    concept_data = candidate
                    used_concept = concept

            if concept_data is None:
                results[metric_name] = {"error": f"No XBRL data found for '{metric_name}'"}
                continue

            # Extract values from the appropriate unit
            units = concept_data.get("units", {})
            # Try common currency units; foreign filers may use local currency
            values = (
                units.get("USD")
                or units.get("USD/shares")
                or units.get("shares")
                # Foreign currencies (common for IFRS filers)
                or units.get("TWD")   # Taiwan Dollar (TSM)
                or units.get("EUR")   # Euro (ASML, SAP)
                or units.get("DKK")   # Danish Krone (NVO)
                or units.get("GBP")   # British Pound
                or units.get("JPY")   # Japanese Yen
                or units.get("KRW")   # Korean Won
                or units.get("CHF")   # Swiss Franc
                # Fallback: grab first available unit
                or (list(units.values())[0] if units else [])
            )

            # Determine the currency from the unit keys
            unit_label = "USD"
            for currency_key in ["USD", "USD/shares", "shares", "TWD", "EUR", "DKK", "GBP", "JPY", "KRW", "CHF"]:
                if units.get(currency_key):
                    unit_label = currency_key
                    break

            # Filter to annual entries and deduplicate by fiscal year
            annual_data = []
            seen_years: set[int] = set()
            for entry in values:
                form = entry.get("form") or ""
                fy = entry.get("fy")
                fp = entry.get("fp") or ""
                if form in annual_forms and fp == "FY" and fy and fy not in seen_years:
                    seen_years.add(fy)
                    annual_data.append({
                        "fiscal_year": fy,
                        "value": entry["val"],
                        "filed": entry.get("filed", ""),
                    })

            annual_data.sort(key=lambda x: x["fiscal_year"], reverse=True)
            annual_data = annual_data[:10]

            # Also get most recent quarterly data
            quarterly_data = []
            seen_quarters: set[str] = set()
            for entry in values:
                form = entry.get("form") or ""
                fy = entry.get("fy")
                fp = entry.get("fp") or ""
                key = f"{fy}-{fp}"
                if form in quarterly_forms and fp.startswith("Q") and key not in seen_quarters:
                    seen_quarters.add(key)
                    quarterly_data.append({
                        "fiscal_year": fy,
                        "fiscal_period": fp,
                        "value": entry["val"],
                        "filed": entry.get("filed", ""),
                    })

            quarterly_data.sort(
                key=lambda x: (x["fiscal_year"], x["fiscal_period"]),
                reverse=True,
            )
            quarterly_data = quarterly_data[:8]

            results[metric_name] = {
                "xbrl_concept": used_concept,
                "label": concept_data.get("label", metric_name),
                "unit": unit_label,
                "annual": annual_data,
                "quarterly": quarterly_data,
            }

        return {
            "ticker": ticker.upper(),
            "company_name": data.get("entityName", ""),
            "data_source": "SEC EDGAR XBRL",
            "accounting_standard": accounting_standard,
            "metrics": results,
        }

    except requests.exceptions.HTTPError as e:
        return {"error": f"SEC EDGAR HTTP error for {ticker}: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to fetch SEC financial data for {ticker}: {str(e)}"}


@tool
def get_insider_trades(ticker: str, limit: int = 20) -> dict[str, Any]:
    """Get insider trading activity from SEC EDGAR (Forms 3, 4, 5).

    Returns recent insider transactions including buys, sells, and
    option exercises by company officers, directors, and 10% owners.
    Insider buying is often seen as a bullish signal.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT').
        limit: Maximum number of transactions to return (default: 20).
    """
    try:
        cik = _ticker_to_cik(ticker)
        if cik is None:
            return {"error": f"Could not find SEC CIK for ticker '{ticker}'"}

        padded_cik = _pad_cik(cik)
        url = f"{SEC_BASE}/submissions/CIK{padded_cik}.json"
        resp = _sec_get(url)
        data = resp.json()

        # Extract Form 4 filings (insider transactions)
        recent = data.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        dates = recent.get("filingDate", [])
        accessions = recent.get("accessionNumber", [])
        descriptions = recent.get("primaryDocDescription", [])

        insider_filings = []
        for i in range(len(forms)):
            form = forms[i] if i < len(forms) else ""
            if form in ("3", "4", "5", "4/A", "3/A"):
                insider_filings.append({
                    "form_type": form,
                    "filing_date": dates[i] if i < len(dates) else "",
                    "description": descriptions[i] if i < len(descriptions) else "",
                    "accession_number": accessions[i] if i < len(accessions) else "",
                })
                if len(insider_filings) >= limit:
                    break

        # Compute summary stats
        total_form4 = sum(1 for f in forms if f in ("4", "4/A"))

        return {
            "ticker": ticker.upper(),
            "company_name": data.get("name", ""),
            "total_insider_filings_on_record": total_form4,
            "recent_filings": insider_filings,
            "note": "Each Form 4 represents an insider transaction (buy/sell/exercise). "
                    "Cluster of Form 4s in a short period may indicate significant insider activity.",
        }

    except requests.exceptions.HTTPError as e:
        return {"error": f"SEC EDGAR HTTP error for {ticker}: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to fetch insider trades for {ticker}: {str(e)}"}


# =============================================================================
# Tool Registry (for the Decomposer to describe to the LLM)
# =============================================================================

SEC_TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    "get_sec_filings": {
        "description": "Get recent SEC filings (10-K, 10-Q, 8-K, etc.) for a company from EDGAR. Returns filing dates, types, and URLs. No API key needed.",
        "parameters": {
            "ticker": "Stock ticker symbol (e.g., 'AAPL')",
            "filing_type": "SEC form type: '10-K', '10-Q', '8-K', 'DEF 14A', '4', or 'ALL' (default: '10-K')",
            "limit": "Number of filings to return (default: 10)",
        },
    },
    "get_sec_financial_data": {
        "description": "Get historical financial data directly from SEC XBRL filings -- more authoritative than Yahoo Finance. Returns annual and quarterly data for chosen metrics.",
        "parameters": {
            "ticker": "Stock ticker symbol (e.g., 'AAPL')",
            "metrics": "Comma-separated metrics: revenue, net_income, eps, eps_diluted, gross_profit, operating_income, total_assets, total_liabilities, stockholders_equity, cash, long_term_debt, shares_outstanding, operating_cash_flow, capex (default: 'revenue,net_income,eps,total_assets,total_liabilities')",
        },
    },
    "get_insider_trades": {
        "description": "Get recent insider trading activity (Forms 3/4/5) from SEC EDGAR. Shows insider buys, sells, and option exercises.",
        "parameters": {
            "ticker": "Stock ticker symbol (e.g., 'AAPL')",
            "limit": "Number of transactions to return (default: 20)",
        },
    },
}

SEC_TOOLS_BY_NAME: dict[str, Any] = {
    "get_sec_filings": get_sec_filings,
    "get_sec_financial_data": get_sec_financial_data,
    "get_insider_trades": get_insider_trades,
}
