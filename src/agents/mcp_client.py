"""
MCP Client for Financial Datasets Server
Handles communication with the Financial Datasets MCP server
"""

import asyncio
import json
import subprocess
import tempfile
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import httpx
from datetime import datetime, timedelta


@dataclass
class MCPResponse:
    """Structure for MCP server responses"""
    success: bool
    data: Any
    error: Optional[str] = None


class FinancialDatasetsMCPClient:
    """
    Client for communicating with the Financial Datasets MCP server
    Based on: https://github.com/financial-datasets/mcp-server
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.financialdatasets.ai"
        self.session = None
        
    async def __aenter__(self):
        self.session = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    async def get_available_tools(self) -> List[str]:
        """Get list of available MCP tools"""
        return [
            "get_income_statements",
            "get_balance_sheets", 
            "get_cash_flow_statements",
            "get_current_stock_price",
            "get_historical_stock_prices",
            "get_company_news",
            "get_available_crypto_tickers",
            "get_crypto_prices",
            "get_historical_crypto_prices",
            "get_current_crypto_price"
        ]
    
    async def get_income_statements(self, ticker: str, period: str = "annual", limit: int = 5) -> MCPResponse:
        """Get income statements for a company"""
        try:
            url = f"{self.base_url}/income-statements"
            params = {
                "ticker": ticker.upper(),
                "period": period,
                "limit": limit
            }
            
            response = await self.session.get(url, params=params)
            response.raise_for_status()
            
            return MCPResponse(success=True, data=response.json())
            
        except Exception as e:
            return MCPResponse(success=False, data=None, error=str(e))
    
    async def get_balance_sheets(self, ticker: str, period: str = "annual", limit: int = 5) -> MCPResponse:
        """Get balance sheets for a company"""
        try:
            url = f"{self.base_url}/balance-sheets"
            params = {
                "ticker": ticker.upper(),
                "period": period,
                "limit": limit
            }
            
            response = await self.session.get(url, params=params)
            response.raise_for_status()
            
            return MCPResponse(success=True, data=response.json())
            
        except Exception as e:
            return MCPResponse(success=False, data=None, error=str(e))
    
    async def get_cash_flow_statements(self, ticker: str, period: str = "annual", limit: int = 5) -> MCPResponse:
        """Get cash flow statements for a company"""
        try:
            url = f"{self.base_url}/cash-flow-statements"
            params = {
                "ticker": ticker.upper(),
                "period": period,
                "limit": limit
            }
            
            response = await self.session.get(url, params=params)
            response.raise_for_status()
            
            return MCPResponse(success=True, data=response.json())
            
        except Exception as e:
            return MCPResponse(success=False, data=None, error=str(e))
    
    async def get_current_stock_price(self, ticker: str) -> MCPResponse:
        """Get current stock price for a company"""
        try:
            url = f"{self.base_url}/prices/current"
            params = {"ticker": ticker.upper()}
            
            response = await self.session.get(url, params=params)
            response.raise_for_status()
            
            return MCPResponse(success=True, data=response.json())
            
        except Exception as e:
            return MCPResponse(success=False, data=None, error=str(e))
    
    async def get_historical_stock_prices(self, ticker: str, start_date: str, end_date: str) -> MCPResponse:
        """Get historical stock prices for a company"""
        try:
            url = f"{self.base_url}/prices/historical"
            params = {
                "ticker": ticker.upper(),
                "start_date": start_date,
                "end_date": end_date
            }
            
            response = await self.session.get(url, params=params)
            response.raise_for_status()
            
            return MCPResponse(success=True, data=response.json())
            
        except Exception as e:
            return MCPResponse(success=False, data=None, error=str(e))
    
    async def get_company_news(self, ticker: str, limit: int = 10) -> MCPResponse:
        """Get news for a company"""
        try:
            url = f"{self.base_url}/news"
            params = {
                "ticker": ticker.upper(),
                "limit": limit
            }
            
            response = await self.session.get(url, params=params)
            response.raise_for_status()
            
            return MCPResponse(success=True, data=response.json())
            
        except Exception as e:
            return MCPResponse(success=False, data=None, error=str(e))
    
    async def execute_mcp_call(self, tool_name: str, **kwargs) -> MCPResponse:
        """Generic method to execute any MCP tool call"""
        method_map = {
            "get_income_statements": self.get_income_statements,
            "get_balance_sheets": self.get_balance_sheets,
            "get_cash_flow_statements": self.get_cash_flow_statements,
            "get_current_stock_price": self.get_current_stock_price,
            "get_historical_stock_prices": self.get_historical_stock_prices,
            "get_company_news": self.get_company_news,
        }
        
        if tool_name not in method_map:
            return MCPResponse(
                success=False, 
                data=None, 
                error=f"Unknown tool: {tool_name}"
            )
        
        return await method_map[tool_name](**kwargs)


class MCPToolRegistry:
    """Registry of available MCP tools with their parameters"""
    
    TOOLS = {
        "get_income_statements": {
            "description": "Get income statements for a company",
            "parameters": {
                "ticker": {"type": "string", "required": True, "description": "Stock ticker symbol"},
                "period": {"type": "string", "required": False, "default": "annual", "description": "annual or quarterly"},
                "limit": {"type": "integer", "required": False, "default": 5, "description": "Number of periods to return"}
            }
        },
        "get_balance_sheets": {
            "description": "Get balance sheets for a company", 
            "parameters": {
                "ticker": {"type": "string", "required": True, "description": "Stock ticker symbol"},
                "period": {"type": "string", "required": False, "default": "annual", "description": "annual or quarterly"},
                "limit": {"type": "integer", "required": False, "default": 5, "description": "Number of periods to return"}
            }
        },
        "get_cash_flow_statements": {
            "description": "Get cash flow statements for a company",
            "parameters": {
                "ticker": {"type": "string", "required": True, "description": "Stock ticker symbol"},
                "period": {"type": "string", "required": False, "default": "annual", "description": "annual or quarterly"},
                "limit": {"type": "integer", "required": False, "default": 5, "description": "Number of periods to return"}
            }
        },
        "get_current_stock_price": {
            "description": "Get current stock price for a company",
            "parameters": {
                "ticker": {"type": "string", "required": True, "description": "Stock ticker symbol"}
            }
        },
        "get_historical_stock_prices": {
            "description": "Get historical stock prices for a company",
            "parameters": {
                "ticker": {"type": "string", "required": True, "description": "Stock ticker symbol"},
                "start_date": {"type": "string", "required": True, "description": "Start date in YYYY-MM-DD format"},
                "end_date": {"type": "string", "required": True, "description": "End date in YYYY-MM-DD format"}
            }
        },
        "get_company_news": {
            "description": "Get news for a company",
            "parameters": {
                "ticker": {"type": "string", "required": True, "description": "Stock ticker symbol"},
                "limit": {"type": "integer", "required": False, "default": 10, "description": "Number of news articles to return"}
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
        formatted = "Available Financial Data Tools:\n\n"
        
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