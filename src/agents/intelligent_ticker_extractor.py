"""
Intelligent Ticker Extractor - LLM-Powered Natural Language to S&P 500 Ticker Translation
Replaces heuristic-based ticker extraction with intelligent understanding of user queries
"""

import json
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI
from src.data.sp500_companies import (
    SP500_COMPANIES, SECTORS, INDUSTRIES, BUSINESS_CATEGORIES,
    search_companies_by_keywords, search_companies_by_category,
    get_companies_by_sector, get_companies_by_industry, get_company_info
)

logger = logging.getLogger(__name__)

class IntelligentTickerExtractor:
    """
    LLM-powered ticker extraction system that understands natural language queries
    and translates them into relevant S&P 500 ticker symbols.
    """
    
    def __init__(self, openai_client: OpenAI):
        self.client = openai_client
        self.max_retries = 3
        
    def extract_tickers(self, query: str) -> List[str]:
        """
        Main method to extract relevant S&P 500 tickers from natural language query
        
        Args:
            query: Natural language query about stocks/companies
            
        Returns:
            List of S&P 500 ticker symbols
        """
        try:
            # Step 1: Use LLM to understand query intent and identify relevant criteria
            query_analysis = self._analyze_query_intent(query)
            
            # Step 2: Extract tickers based on the analyzed criteria
            tickers = self._extract_tickers_from_analysis(query_analysis)
            
            # Step 3: Validate and filter results
            valid_tickers = self._validate_and_filter_tickers(tickers, query)
            
            logger.info(f"Extracted {len(valid_tickers)} tickers for query: '{query[:100]}...'")
            return valid_tickers
            
        except Exception as e:
            logger.error(f"Error in intelligent ticker extraction: {e}")
            # Fallback to simple keyword search
            return self._fallback_extraction(query)
    
    def _analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """
        Use LLM to analyze the query and extract relevant search criteria
        """
        try:
            system_prompt = f"""You are an expert financial analyst helping to understand natural language queries about S&P 500 companies.

Your task is to analyze the user's query and extract relevant criteria for finding companies. 

Available S&P 500 sectors: {list(SECTORS.keys())}
Available industries: {list(INDUSTRIES.keys())}
Available business categories: {list(BUSINESS_CATEGORIES.keys())}

Please analyze the query and return a JSON response with these fields:
{{
    "intent": "description of what the user is looking for",
    "sectors": ["list of relevant sectors from available sectors"],
    "industries": ["list of relevant industries from available industries"], 
    "business_categories": ["list of relevant business categories"],
    "keywords": ["list of relevant keywords"],
    "financial_criteria": {{
        "market_cap": {{"min": null, "max": null, "description": ""}},
        "revenue_growth": {{"min": null, "description": ""}},
        "performance": {{"type": "", "description": ""}}
    }},
    "specific_companies": ["list of specific company names or tickers mentioned"],
    "company_count": {{"type": "exact|approximate|all", "number": null}}
}}

Examples:
- "car manufacturers in SP500" → sectors: ["Consumer Discretionary"], industries: ["Automobiles"], business_categories: ["car manufacturers"]
- "tech companies with high growth" → sectors: ["Information Technology"], keywords: ["technology", "growth"]
- "all energy companies" → sectors: ["Energy"], company_count: {{"type": "all"}}
- "top 5 banks by market cap" → industries: ["Banks"], financial_criteria: {{"market_cap": {{"description": "largest"}}}}, company_count: {{"type": "exact", "number": 5}}
- "companies with revenue growth > 20%" → financial_criteria: {{"revenue_growth": {{"min": 20}}}}

User Query: {query}"""

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean JSON response (remove markdown if present)
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            analysis = json.loads(content)
            logger.info(f"Query analysis: {analysis}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error in query analysis: {e}")
            # Return basic analysis
            return {
                "intent": "Find companies related to the query",
                "sectors": [],
                "industries": [],
                "business_categories": [],
                "keywords": [query.lower()],
                "financial_criteria": {},
                "specific_companies": [],
                "company_count": {"type": "all", "number": None}
            }
    
    def _extract_tickers_from_analysis(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Extract tickers based on the analyzed criteria
        """
        tickers = set()
        
        # 1. Handle specific companies mentioned
        if analysis.get("specific_companies"):
            for company in analysis["specific_companies"]:
                company_tickers = self._find_company_by_name(company)
                tickers.update(company_tickers)
        
        # 2. Handle sectors
        if analysis.get("sectors"):
            for sector in analysis["sectors"]:
                sector_tickers = get_companies_by_sector(sector)
                tickers.update(sector_tickers)
        
        # 3. Handle industries  
        if analysis.get("industries"):
            for industry in analysis["industries"]:
                industry_tickers = get_companies_by_industry(industry)
                tickers.update(industry_tickers)
        
        # 4. Handle business categories
        if analysis.get("business_categories"):
            for category in analysis["business_categories"]:
                category_tickers = search_companies_by_category(category)
                tickers.update(category_tickers)
        
        # 5. Handle keywords
        if analysis.get("keywords"):
            keyword_tickers = search_companies_by_keywords(analysis["keywords"])
            tickers.update(keyword_tickers)
        
        # 6. If no specific criteria found, try broader search
        if not tickers and analysis.get("intent"):
            broad_tickers = search_companies_by_keywords([analysis["intent"]])
            tickers.update(broad_tickers)
        
        return list(tickers)
    
    def _find_company_by_name(self, company_name: str) -> List[str]:
        """
        Find ticker by company name (fuzzy matching)
        """
        company_lower = company_name.lower()
        matches = []
        
        for ticker, info in SP500_COMPANIES.items():
            # Check exact name match
            if company_lower in info["name"].lower():
                matches.append(ticker)
                continue
            
            # Check if company name contains the search term
            name_words = info["name"].lower().split()
            search_words = company_lower.split()
            
            if any(search_word in name_words for search_word in search_words):
                matches.append(ticker)
                continue
            
            # Check keywords
            if any(company_lower in keyword for keyword in info["keywords"]):
                matches.append(ticker)
        
        return matches
    
    def _validate_and_filter_tickers(self, tickers: List[str], original_query: str) -> List[str]:
        """
        Validate tickers and apply intelligent filtering based on query context
        """
        if not tickers:
            return []
        
        # Remove duplicates and ensure all are valid S&P 500 tickers
        valid_tickers = [t for t in set(tickers) if t in SP500_COMPANIES]
        
        # If we have too many results, use LLM to rank and filter
        if len(valid_tickers) > 20:
            valid_tickers = self._rank_and_filter_tickers(valid_tickers, original_query)
        
        return valid_tickers[:50]  # Cap at 50 results max
    
    def _rank_and_filter_tickers(self, tickers: List[str], query: str) -> List[str]:
        """
        Use LLM to rank and filter tickers when there are too many results
        """
        try:
            # Prepare company information for ranking
            companies_info = []
            for ticker in tickers[:100]:  # Limit for context size
                info = SP500_COMPANIES[ticker]
                companies_info.append({
                    "ticker": ticker,
                    "name": info["name"],
                    "sector": info["sector"],
                    "industry": info["industry"],
                    "description": info["description"][:200]  # Truncate for context
                })
            
            system_prompt = f"""You are a financial expert helping to rank and filter S&P 500 companies based on relevance to a user query.

Given the user query and a list of potentially relevant companies, please:
1. Rank the companies by relevance to the query
2. Return the top 20 most relevant companies
3. Exclude companies that don't actually match the query intent

User Query: {query}

Available Companies: {json.dumps(companies_info, indent=2)}

Please return a JSON array of ticker symbols in order of relevance (most relevant first):
["TICKER1", "TICKER2", "TICKER3", ...]

Only include tickers that are truly relevant to the query. Maximum 20 tickers."""

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean JSON response
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            ranked_tickers = json.loads(content)
            
            # Validate that all returned tickers are in our original list
            filtered_tickers = [t for t in ranked_tickers if t in tickers]
            
            logger.info(f"Ranked and filtered from {len(tickers)} to {len(filtered_tickers)} tickers")
            return filtered_tickers
            
        except Exception as e:
            logger.error(f"Error in ranking tickers: {e}")
            # Fallback: return first 20 tickers
            return tickers[:20]
    
    def _fallback_extraction(self, query: str) -> List[str]:
        """
        Fallback method when LLM extraction fails - uses simple keyword matching
        """
        logger.warning("Using fallback ticker extraction")
        
        # Simple keyword search
        words = query.lower().split()
        tickers = search_companies_by_keywords(words)
        
        # Try business categories
        for category in BUSINESS_CATEGORIES:
            if category in query.lower():
                tickers.extend(search_companies_by_category(category))
        
        return list(set(tickers))[:20]  # Return unique tickers, max 20
    
    def get_extraction_explanation(self, query: str, tickers: List[str]) -> str:
        """
        Generate an explanation of why these tickers were selected for the query
        """
        if not tickers:
            return f"No S&P 500 companies found matching the query: '{query}'"
        
        # Group tickers by sector for explanation
        sectors_found = {}
        for ticker in tickers[:10]:  # Limit for explanation
            info = SP500_COMPANIES.get(ticker, {})
            sector = info.get("sector", "Unknown")
            if sector not in sectors_found:
                sectors_found[sector] = []
            sectors_found[sector].append(f"{ticker} ({info.get('name', '')})")
        
        explanation = f"Found {len(tickers)} S&P 500 companies for query: '{query}'\n\n"
        
        for sector, companies in sectors_found.items():
            explanation += f"{sector}:\n"
            for company in companies[:5]:  # Show max 5 per sector
                explanation += f"  - {company}\n"
            if len(companies) > 5:
                explanation += f"  - ... and {len(companies) - 5} more\n"
            explanation += "\n"
        
        if len(tickers) > 10:
            explanation += f"... and {len(tickers) - 10} more companies"
        
        return explanation

# Convenience function for backward compatibility
def extract_tickers(query: str, openai_client: OpenAI = None) -> List[str]:
    """
    Backward compatible function for extracting tickers from natural language query
    """
    if openai_client is None:
        # If no OpenAI client provided, fall back to simple keyword search
        words = query.lower().split()
        return search_companies_by_keywords(words)[:20]
    
    extractor = IntelligentTickerExtractor(openai_client)
    return extractor.extract_tickers(query) 