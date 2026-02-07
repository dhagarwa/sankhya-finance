"""
Query Generator -- produces diverse equity analysis queries for testing.
"""

import random
from typing import Any

QUERY_TEMPLATES: list[dict[str, Any]] = [
    {"template": "What is {company}'s current stock price and market cap?", "category": "price", "expected_tools": ["get_current_stock_price"]},
    {"template": "Show me {ticker}'s stock performance over the last 6 months", "category": "price_history", "expected_tools": ["get_historical_stock_prices"]},
    {"template": "Analyze {company}'s revenue and earnings growth over the past 3 years", "category": "fundamental_growth", "expected_tools": ["get_income_statements", "get_key_metrics"]},
    {"template": "What are the key financial metrics for {ticker}?", "category": "fundamental_snapshot", "expected_tools": ["get_key_metrics"]},
    {"template": "Show me {company}'s balance sheet and debt levels", "category": "fundamental_balance", "expected_tools": ["get_balance_sheets"]},
    {"template": "What is {ticker}'s free cash flow and how has it trended?", "category": "fundamental_cashflow", "expected_tools": ["get_cash_flow_statements"]},
    {"template": "What is {company}'s P/E ratio and how does it compare to the industry average?", "category": "valuation", "expected_tools": ["get_key_metrics"]},
    {"template": "When was {company}'s most recent 10-K filing and what did it show?", "category": "sec_filings", "expected_tools": ["get_sec_filings"]},
    {"template": "Show me {ticker}'s revenue from SEC filings for the last 5 years", "category": "sec_financials", "expected_tools": ["get_sec_financial_data"]},
    {"template": "Has there been any insider buying or selling at {company} recently?", "category": "insider_activity", "expected_tools": ["get_insider_trades"]},
    {"template": "What are Wall Street analysts saying about {ticker}?", "category": "analyst_recs", "expected_tools": ["get_analyst_recommendations"]},
    {"template": "Who are the largest institutional holders of {company}?", "category": "institutional", "expected_tools": ["get_institutional_holders"]},
    {"template": "What does the options market suggest about {ticker}'s near-term direction?", "category": "options_sentiment", "expected_tools": ["get_options_overview"]},
    {"template": "Give me a comprehensive equity analysis of {company} including valuation, growth, and analyst sentiment", "category": "comprehensive", "expected_tools": ["get_key_metrics", "get_income_statements", "get_analyst_recommendations"]},
    {"template": "Is {ticker} a buy right now? Look at fundamentals, analyst ratings, and insider activity", "category": "buy_sell", "expected_tools": ["get_key_metrics", "get_analyst_recommendations", "get_insider_trades"]},
    {"template": "What is the latest news about {company}?", "category": "news", "expected_tools": ["get_company_news", "web_news_search"]},
]


def generate_query(ticker: str, company_name: str, seed: int | None = None) -> dict[str, str]:
    """Generate a random equity analysis query for a given company."""
    if seed is None:
        seed = sum(ord(c) for c in ticker)
    rng = random.Random(seed)
    template_info = rng.choice(QUERY_TEMPLATES)
    query = template_info["template"].format(ticker=ticker, company=company_name)
    return {
        "query": query,
        "category": template_info["category"],
        "expected_tools": template_info["expected_tools"],
        "ticker": ticker,
        "company": company_name,
    }


def generate_all_queries(companies: dict[str, dict]) -> list[dict[str, str]]:
    """Generate one query per company."""
    return [generate_query(t, i["name"]) for t, i in sorted(companies.items())]
