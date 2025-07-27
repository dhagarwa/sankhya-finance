"""
YFinance Client - Direct access to Yahoo Finance data
Provides the same interface as MCP client but uses yfinance directly
"""

import asyncio
import yfinance as yf
import pandas as pd
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta, date
import warnings

# Suppress yfinance warnings
warnings.filterwarnings("ignore", module="yfinance")


@dataclass
class FinanceResponse:
    """Structure for finance data responses"""
    success: bool
    data: Any
    error: Optional[str] = None


class YFinanceClient:
    """
    Simple client that uses yfinance directly to get financial data
    Compatible with the MCP client interface for easy replacement
    """
    
    def __init__(self):
        self.session = None
        
    async def __aenter__(self):
        # No session needed for yfinance
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # No cleanup needed
        pass
    
    async def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        return [
            "get_income_statements",
            "get_balance_sheets", 
            "get_cash_flow_statements",
            "get_current_stock_price",
            "get_historical_stock_prices",
            "get_company_news",
            "get_company_info"
        ]
    
    def _run_async(self, func, *args, **kwargs):
        """Helper to run sync yfinance calls in async context"""
        return asyncio.get_event_loop().run_in_executor(None, func, *args, **kwargs)
    
    async def get_income_statements(self, ticker: str, period: str = "annual", limit: int = 5) -> FinanceResponse:
        """Get income statements for a company"""
        try:
            stock = yf.Ticker(ticker.upper())
            
            if period.lower() == "quarterly":
                data = await self._run_async(lambda: stock.quarterly_financials)
            else:
                data = await self._run_async(lambda: stock.financials)
            
            if data.empty:
                return FinanceResponse(success=False, data=None, error=f"No income statement data found for {ticker}")
            
            # Limit the number of periods and convert to dict
            limited_data = data.iloc[:, :limit] if len(data.columns) > limit else data
            result = {
                "ticker": ticker.upper(),
                "period": period,
                "data": limited_data.to_dict()
            }
            
            return FinanceResponse(success=True, data=result)
            
        except Exception as e:
            return FinanceResponse(success=False, data=None, error=str(e))
    
    async def get_balance_sheets(self, ticker: str, period: str = "annual", limit: int = 5) -> FinanceResponse:
        """Get balance sheets for a company"""
        try:
            stock = yf.Ticker(ticker.upper())
            
            if period.lower() == "quarterly":
                data = await self._run_async(lambda: stock.quarterly_balance_sheet)
            else:
                data = await self._run_async(lambda: stock.balance_sheet)
            
            if data.empty:
                return FinanceResponse(success=False, data=None, error=f"No balance sheet data found for {ticker}")
            
            # Limit the number of periods and convert to dict
            limited_data = data.iloc[:, :limit] if len(data.columns) > limit else data
            result = {
                "ticker": ticker.upper(),
                "period": period,
                "data": limited_data.to_dict()
            }
            
            return FinanceResponse(success=True, data=result)
            
        except Exception as e:
            return FinanceResponse(success=False, data=None, error=str(e))
    
    async def get_cash_flow_statements(self, ticker: str, period: str = "annual", limit: int = 5) -> FinanceResponse:
        """Get cash flow statements for a company"""
        try:
            stock = yf.Ticker(ticker.upper())
            
            if period.lower() == "quarterly":
                data = await self._run_async(lambda: stock.quarterly_cashflow)
            else:
                data = await self._run_async(lambda: stock.cashflow)
            
            if data.empty:
                return FinanceResponse(success=False, data=None, error=f"No cash flow data found for {ticker}")
            
            # Limit the number of periods and convert to dict
            limited_data = data.iloc[:, :limit] if len(data.columns) > limit else data
            result = {
                "ticker": ticker.upper(),
                "period": period,
                "data": limited_data.to_dict()
            }
            
            return FinanceResponse(success=True, data=result)
            
        except Exception as e:
            return FinanceResponse(success=False, data=None, error=str(e))
    
    async def get_current_stock_price(self, ticker: str) -> FinanceResponse:
        """Get current stock price for a company"""
        try:
            stock = yf.Ticker(ticker.upper())
            info = await self._run_async(lambda: stock.info)
            
            if not info:
                return FinanceResponse(success=False, data=None, error=f"No data found for ticker {ticker}")
            
            # Get current price from different possible fields
            current_price = (
                info.get('currentPrice') or 
                info.get('regularMarketPrice') or 
                info.get('previousClose')
            )
            
            if current_price is None:
                return FinanceResponse(success=False, data=None, error=f"No current price data available for {ticker}")
            
            result = {
                "ticker": ticker.upper(),
                "currentPrice": current_price,
                "currency": info.get('currency', 'USD'),
                "marketCap": info.get('marketCap'),
                "companyName": info.get('longName', info.get('shortName')),
                "lastUpdate": datetime.now().isoformat()
            }
            
            return FinanceResponse(success=True, data=result)
            
        except Exception as e:
            return FinanceResponse(success=False, data=None, error=str(e))
    
    async def get_historical_stock_prices(self, ticker: str, start_date: str, end_date: str) -> FinanceResponse:
        """Get historical stock prices for a company"""
        try:
            stock = yf.Ticker(ticker.upper())
            
            # Download historical data
            data = await self._run_async(
                lambda: stock.history(start=start_date, end=end_date)
            )
            
            if data.empty:
                return FinanceResponse(success=False, data=None, error=f"No historical data found for {ticker}")
            
            # Convert to dict with readable format
            result = {
                "ticker": ticker.upper(),
                "start_date": start_date,
                "end_date": end_date,
                "data": data.reset_index().to_dict('records')  # Include date as a column
            }
            
            return FinanceResponse(success=True, data=result)
            
        except Exception as e:
            return FinanceResponse(success=False, data=None, error=str(e))
    
    async def get_company_news(self, ticker: str, limit: int = 10) -> FinanceResponse:
        """Get news for a company"""
        try:
            stock = yf.Ticker(ticker.upper())
            news = await self._run_async(lambda: stock.news)
            
            if not news:
                return FinanceResponse(success=False, data=None, error=f"No news found for {ticker}")
            
            # Limit news articles and format
            limited_news = news[:limit] if len(news) > limit else news
            
            result = {
                "ticker": ticker.upper(),
                "news": limited_news
            }
            
            return FinanceResponse(success=True, data=result)
            
        except Exception as e:
            return FinanceResponse(success=False, data=None, error=str(e))
    
    async def get_company_info(self, ticker: str) -> FinanceResponse:
        """Get basic company information"""
        try:
            stock = yf.Ticker(ticker.upper())
            info = await self._run_async(lambda: stock.info)
            
            if not info:
                return FinanceResponse(success=False, data=None, error=f"No company info found for {ticker}")
            
            # Extract key info
            result = {
                "ticker": ticker.upper(),
                "companyName": info.get('longName', info.get('shortName')),
                "sector": info.get('sector'),
                "industry": info.get('industry'),
                "website": info.get('website'),
                "summary": info.get('longBusinessSummary'),
                "employees": info.get('fullTimeEmployees'),
                "marketCap": info.get('marketCap'),
                "currency": info.get('currency', 'USD')
            }
            
            return FinanceResponse(success=True, data=result)
            
        except Exception as e:
            return FinanceResponse(success=False, data=None, error=str(e))
    
    async def execute_mcp_call(self, tool_name: str, **kwargs) -> FinanceResponse:
        """Generic method to execute any tool call"""
        method_map = {
            "get_income_statements": self.get_income_statements,
            "get_balance_sheets": self.get_balance_sheets,
            "get_cash_flow_statements": self.get_cash_flow_statements,
            "get_current_stock_price": self.get_current_stock_price,
            "get_historical_stock_prices": self.get_historical_stock_prices,
            "get_company_news": self.get_company_news,
            "get_company_info": self.get_company_info,
        }
        
        if tool_name not in method_map:
            return FinanceResponse(
                success=False, 
                data=None, 
                error=f"Unknown tool: {tool_name}"
            )
        
        return await method_map[tool_name](**kwargs)


class FinanceToolRegistry:
    """Registry of available finance tools with their parameters"""
    
    TOOLS = {
        "get_income_statements": {
            "description": "Get income statements for a company using Yahoo Finance",
            "parameters": {
                "ticker": {"type": "string", "required": True, "description": "Stock ticker symbol"},
                "period": {"type": "string", "required": False, "default": "annual", "description": "annual or quarterly"},
                "limit": {"type": "integer", "required": False, "default": 5, "description": "Number of periods to return"}
            }
        },
        "get_balance_sheets": {
            "description": "Get balance sheets for a company using Yahoo Finance", 
            "parameters": {
                "ticker": {"type": "string", "required": True, "description": "Stock ticker symbol"},
                "period": {"type": "string", "required": False, "default": "annual", "description": "annual or quarterly"},
                "limit": {"type": "integer", "required": False, "default": 5, "description": "Number of periods to return"}
            }
        },
        "get_cash_flow_statements": {
            "description": "Get cash flow statements for a company using Yahoo Finance",
            "parameters": {
                "ticker": {"type": "string", "required": True, "description": "Stock ticker symbol"},
                "period": {"type": "string", "required": False, "default": "annual", "description": "annual or quarterly"},
                "limit": {"type": "integer", "required": False, "default": 5, "description": "Number of periods to return"}
            }
        },
        "get_current_stock_price": {
            "description": "Get current stock price for a company using Yahoo Finance",
            "parameters": {
                "ticker": {"type": "string", "required": True, "description": "Stock ticker symbol"}
            }
        },
        "get_historical_stock_prices": {
            "description": "Get historical stock prices for a company using Yahoo Finance",
            "parameters": {
                "ticker": {"type": "string", "required": True, "description": "Stock ticker symbol"},
                "start_date": {"type": "string", "required": True, "description": "Start date in YYYY-MM-DD format"},
                "end_date": {"type": "string", "required": True, "description": "End date in YYYY-MM-DD format"}
            }
        },
        "get_company_news": {
            "description": "Get recent news for a company using Yahoo Finance",
            "parameters": {
                "ticker": {"type": "string", "required": True, "description": "Stock ticker symbol"},
                "limit": {"type": "integer", "required": False, "default": 10, "description": "Number of news articles to return"}
            }
        },
        "get_company_info": {
            "description": "Get basic company information using Yahoo Finance",
            "parameters": {
                "ticker": {"type": "string", "required": True, "description": "Stock ticker symbol"}
            }
        }
    }
    
    @classmethod
    def get_tool_info(cls, tool_name: str) -> Optional[Dict]:
        """Get information about a specific tool"""
        return cls.TOOLS.get(tool_name)
    
    @classmethod
    def get_all_tools(cls) -> Dict[str, Dict]:
        """Get information about all available tools"""
        return cls.TOOLS
    
    @classmethod
    def format_tools_for_llm(cls) -> str:
        """Format tool information for LLM consumption"""
        formatted = "Available Financial Data Tools (via Yahoo Finance):\n\n"
        
        for tool_name, tool_info in cls.TOOLS.items():
            formatted += f"**{tool_name}**\n"
            formatted += f"Description: {tool_info['description']}\n"
            formatted += "Parameters:\n"
            
            for param_name, param_info in tool_info['parameters'].items():
                required = "Required" if param_info['required'] else "Optional"
                default = f" (default: {param_info.get('default', 'N/A')})" if not param_info['required'] else ""
                formatted += f"  - {param_name} ({param_info['type']}): {param_info['description']} [{required}]{default}\n"
            
            formatted += "\n"
        
        return formatted 