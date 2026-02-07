"""
Intelligent Ticker Extractor - Consolidated from v1.

Translates natural language queries into S&P 500 ticker symbols using
LLM-powered understanding. This replaces TWO separate implementations
from v1:
    - intelligent_ticker_extractor.py  (full LLM-powered extractor)
    - QueryPatterns.extract_tickers()  (duplicated hardcoded company map)

How it works:
    1. Send the query to the LLM with the list of available sectors,
       industries, and business categories from our S&P 500 database.
    2. The LLM returns structured criteria (sectors, industries, keywords,
       specific company names).
    3. We search the S&P 500 database using those criteria.
    4. If too many results, we ask the LLM to rank and filter them.
    5. If the LLM call fails, we fall back to simple keyword matching.

Usage:
    tickers = extract_tickers("car manufacturers in SP500", llm)
"""

import json
import logging
from typing import Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from src.data.sp500_companies import (
    SP500_COMPANIES,
    SECTORS,
    INDUSTRIES,
    BUSINESS_CATEGORIES,
    search_companies_by_keywords,
    search_companies_by_category,
    get_companies_by_sector,
    get_companies_by_industry,
)

logger = logging.getLogger(__name__)


# =============================================================================
# Main Public Function
# =============================================================================


def extract_tickers(query: str, llm: ChatOpenAI) -> list[str]:
    """
    Extract relevant S&P 500 ticker symbols from a natural language query.

    This is the single entry point for ticker extraction. It uses the LLM
    to understand the query intent, then searches the S&P 500 database.

    Args:
        query: Natural language query (e.g., "car manufacturers in SP500").
        llm:   A configured ChatOpenAI instance from get_llm().

    Returns:
        List of ticker symbols (e.g., ["TSLA", "F", "GM"]).
        Empty list if no relevant tickers found.
    """
    try:
        # Step 1: Use LLM to understand query intent
        analysis = _analyze_query_intent(query, llm)

        # Step 2: Search S&P 500 database based on analysis
        tickers = _search_by_criteria(analysis)

        # Step 3: If too many results, ask LLM to rank and filter
        if len(tickers) > 20:
            tickers = _rank_and_filter(tickers, query, llm)

        # Step 4: Validate all tickers are in our database
        valid_tickers = [t for t in tickers if t in SP500_COMPANIES]

        # Cap at 50 results maximum
        return valid_tickers[:50]

    except Exception as e:
        logger.warning(f"LLM ticker extraction failed, using fallback: {e}")
        return _fallback_extraction(query)


# =============================================================================
# Internal Functions
# =============================================================================


def _analyze_query_intent(query: str, llm: ChatOpenAI) -> dict[str, Any]:
    """
    Use the LLM to understand what companies/sectors the user is asking about.

    Returns a structured dict with fields like:
        {
            "sectors": ["Information Technology"],
            "industries": ["Semiconductors"],
            "business_categories": ["chip makers"],
            "keywords": ["semiconductor", "chips"],
            "specific_companies": ["NVIDIA", "AMD"],
        }
    """
    system_prompt = f"""You are an expert financial analyst helping to understand natural language queries about S&P 500 companies.

Analyze the user's query and extract criteria for finding relevant companies.

Available S&P 500 sectors: {list(SECTORS.keys())}
Available industries (sample): {list(INDUSTRIES.keys())[:30]}
Available business categories: {list(BUSINESS_CATEGORIES.keys())}

Return a JSON object with these fields:
{{
    "intent": "brief description of what the user wants",
    "sectors": ["relevant sectors from the list above"],
    "industries": ["relevant industries"],
    "business_categories": ["relevant categories"],
    "keywords": ["search keywords"],
    "specific_companies": ["specific company names or tickers mentioned"]
}}

Rules:
- Only use sectors/industries/categories that exist in the lists above
- If the user mentions specific companies by name, include them in specific_companies
- If the query is about a broad category (e.g., "tech companies"), use sectors
- If the query is about a narrow category (e.g., "chip makers"), use business_categories
- Return ONLY valid JSON, no additional text"""

    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=query),
        ])

        content = response.content.strip()

        # Clean markdown code blocks if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        return json.loads(content.strip())

    except Exception as e:
        logger.warning(f"Query intent analysis failed: {e}")
        # Return basic analysis so we can still try keyword search
        return {
            "intent": query,
            "sectors": [],
            "industries": [],
            "business_categories": [],
            "keywords": query.lower().split(),
            "specific_companies": [],
        }


def _search_by_criteria(analysis: dict[str, Any]) -> list[str]:
    """
    Search the S&P 500 database using the criteria from LLM analysis.

    Searches multiple dimensions (sectors, industries, categories, keywords,
    specific companies) and unions the results.
    """
    tickers: set[str] = set()

    # 1. Specific company names or tickers mentioned directly
    for company in analysis.get("specific_companies", []):
        tickers.update(_find_company_by_name(company))

    # 2. Sector-based search
    for sector in analysis.get("sectors", []):
        tickers.update(get_companies_by_sector(sector))

    # 3. Industry-based search
    for industry in analysis.get("industries", []):
        tickers.update(get_companies_by_industry(industry))

    # 4. Business category search
    for category in analysis.get("business_categories", []):
        tickers.update(search_companies_by_category(category))

    # 5. Keyword search
    keywords = analysis.get("keywords", [])
    if keywords:
        tickers.update(search_companies_by_keywords(keywords))

    # 6. If nothing found, try broader search using the intent
    if not tickers and analysis.get("intent"):
        intent_words = analysis["intent"].lower().split()
        tickers.update(search_companies_by_keywords(intent_words))

    return list(tickers)


def _find_company_by_name(name: str) -> list[str]:
    """
    Find ticker(s) by company name using fuzzy matching.

    Checks the company name, individual words, and keywords
    in the S&P 500 database.
    """
    name_lower = name.lower()
    matches = []

    for ticker, info in SP500_COMPANIES.items():
        # Check if search term appears in company name
        if name_lower in info["name"].lower():
            matches.append(ticker)
            continue

        # Check if any word in the search term matches a word in the name
        name_words = info["name"].lower().split()
        search_words = name_lower.split()
        if any(sw in name_words for sw in search_words):
            matches.append(ticker)
            continue

        # Check keywords
        if any(name_lower in kw for kw in info.get("keywords", [])):
            matches.append(ticker)

        # Check if it's a ticker symbol directly
        if name.upper() == ticker:
            matches.append(ticker)

    return matches


def _rank_and_filter(
    tickers: list[str],
    query: str,
    llm: ChatOpenAI,
) -> list[str]:
    """
    When we have too many results (>20), ask the LLM to rank by relevance
    and return the top 20.
    """
    try:
        # Prepare company info for the LLM (limit to first 100 for context size)
        companies_info = []
        for ticker in tickers[:100]:
            info = SP500_COMPANIES[ticker]
            companies_info.append({
                "ticker": ticker,
                "name": info["name"],
                "sector": info["sector"],
                "industry": info["industry"],
            })

        prompt = f"""Given this query: "{query}"

And these potentially relevant S&P 500 companies:
{json.dumps(companies_info, indent=2)}

Return a JSON array of the top 20 most relevant ticker symbols, ordered by relevance:
["TICKER1", "TICKER2", ...]

Only include companies truly relevant to the query. Return ONLY the JSON array."""

        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()

        # Clean markdown
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        ranked = json.loads(content.strip())

        # Only return tickers that were in our original list
        return [t for t in ranked if t in tickers]

    except Exception as e:
        logger.warning(f"Ranking failed, returning first 20: {e}")
        return tickers[:20]


def _fallback_extraction(query: str) -> list[str]:
    """
    Fallback when LLM extraction fails entirely.
    Uses simple keyword matching against the S&P 500 database.
    """
    logger.info("Using fallback keyword-based ticker extraction")

    tickers: set[str] = set()

    # Keyword search
    words = query.lower().split()
    tickers.update(search_companies_by_keywords(words))

    # Business category search
    for category in BUSINESS_CATEGORIES:
        if category in query.lower():
            tickers.update(search_companies_by_category(category))

    return list(tickers)[:20]
