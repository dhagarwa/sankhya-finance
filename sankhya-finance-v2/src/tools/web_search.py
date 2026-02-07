"""
Web Search Tools for LangGraph.

Provides general web search and web news search capabilities using
DuckDuckGo (free, no API key required). These complement the Yahoo Finance
tools by allowing the agent to find information that isn't available
through financial APIs alone -- e.g., recent announcements, regulatory
filings context, industry trends, or analyst commentary.

The Decomposer can choose these tools for DATA steps when:
    - The query needs context beyond raw financial numbers
    - Recent news or events are relevant to the analysis
    - The user asks about something not covered by YFinance APIs
"""

from datetime import datetime
from typing import Any

from langchain_core.tools import tool


# =============================================================================
# Tool Implementations
# =============================================================================


@tool
def web_search(query: str, max_results: int = 5) -> dict[str, Any]:
    """Search the web for general information using DuckDuckGo.

    Use this for finding context, explanations, analyst opinions,
    industry trends, or any information not available from Yahoo Finance.

    Args:
        query: Search query string (e.g., 'NVIDIA AI revenue drivers 2024').
        max_results: Maximum number of results to return. Defaults to 5.
    """
    try:
        from ddgs import DDGS

        results = list(DDGS().text(query, max_results=max_results))

        if not results:
            return {"error": f"No web search results found for: {query}"}

        cleaned_results = []
        for r in results:
            cleaned_results.append({
                "title": r.get("title", ""),
                "snippet": r.get("body", ""),
                "url": r.get("href", ""),
            })

        return {
            "query": query,
            "result_count": len(cleaned_results),
            "results": cleaned_results,
            "searched_at": datetime.now().isoformat(),
        }

    except ImportError:
        return {"error": "ddgs not installed. Run: pip install ddgs"}
    except Exception as e:
        return {"error": f"Web search failed for '{query}': {str(e)}"}


@tool
def web_news_search(query: str, max_results: int = 5) -> dict[str, Any]:
    """Search the web specifically for recent NEWS articles using DuckDuckGo News.

    Better than get_company_news (Yahoo Finance) when you need broader news
    coverage, non-company-specific news, or industry/macro news.

    Args:
        query: News search query (e.g., 'NVIDIA earnings report Q4 2025').
        max_results: Maximum number of articles to return. Defaults to 5.
    """
    try:
        from ddgs import DDGS

        results = list(DDGS().news(query, max_results=max_results))

        if not results:
            return {"error": f"No news results found for: {query}"}

        cleaned_results = []
        for r in results:
            cleaned_results.append({
                "title": r.get("title", ""),
                "snippet": r.get("body", ""),
                "url": r.get("url", r.get("href", "")),
                "source": r.get("source", ""),
                "date": r.get("date", ""),
            })

        return {
            "query": query,
            "result_count": len(cleaned_results),
            "articles": cleaned_results,
            "searched_at": datetime.now().isoformat(),
        }

    except ImportError:
        return {"error": "ddgs not installed. Run: pip install ddgs"}
    except Exception as e:
        return {"error": f"Web news search failed for '{query}': {str(e)}"}


# =============================================================================
# Tool Registry Entries (for the Decomposer to describe to the LLM)
# =============================================================================

WEB_TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    "web_search": {
        "description": "Search the web for general information, context, analyst opinions, industry trends, or anything not in Yahoo Finance data",
        "parameters": {
            "query": "Search query string (e.g., 'NVIDIA AI revenue drivers 2024')",
            "max_results": "Number of results to return (default: 5)",
        },
    },
    "web_news_search": {
        "description": "Search the web specifically for recent news articles -- broader coverage than Yahoo Finance news",
        "parameters": {
            "query": "News search query (e.g., 'NVIDIA earnings report Q4 2025')",
            "max_results": "Number of articles to return (default: 5)",
        },
    },
}

WEB_TOOLS_BY_NAME: dict[str, Any] = {
    "web_search": web_search,
    "web_news_search": web_news_search,
}
