from typing import Dict, List, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import sys
from openai import OpenAI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.agents.step_classifier import StepClassifier, AgentType

class DataRequest(BaseModel):
    """Schema for translating decomposed steps into yfinance API calls"""
    metrics: List[str] = Field(description="YFinance metrics to fetch")
    tickers: List[str] = Field(description="Stock symbols to analyze")
    start_date: Optional[str] = Field(description="Start date for historical data")
    end_date: Optional[str] = Field(description="End date for historical data")
    frequency: Optional[str] = Field(description="Data frequency (1d, 1wk, 1mo, 1q)")

class DataRetrievalAgent:
    """
    Agent responsible for executing the data retrieval plan created by QueryDecomposer
    using YFinance APIs.
    """
    
    def __init__(self):

        self.llm = ChatOpenAI(
            model="gpt-4-0125-preview",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Define available YFinance metrics as class attribute
        self.AVAILABLE_METRICS = {
            # Market Data
            'price': ['currentPrice', 'previousClose', 'open', 'dayLow', 'dayHigh'],
            'volume': ['volume', 'averageVolume', 'averageVolume10days'],
            'market_stats': ['marketCap', 'impliedSharesOutstanding', 'sharesOutstanding', 'floatShares'],
            'moving_averages': ['fiftyDayAverage', 'twoHundredDayAverage'],
            
            # Valuation
            'pe_ratios': ['trailingPE', 'forwardPE', 'trailingPegRatio'],
            'price_ratios': ['priceToBook', 'priceToSalesTrailing12Months'],
            'enterprise': ['enterpriseValue', 'enterpriseToRevenue', 'enterpriseToEbitda'],
            
            # Financial Performance
            'margins': ['profitMargins', 'grossMargins', 'operatingMargins', 'ebitdaMargins'],
            'returns': ['returnOnAssets', 'returnOnEquity'],
            'growth': ['earningsGrowth', 'revenueGrowth', 'earningsQuarterlyGrowth'],
            
            # Income Statement
            'revenue': ['totalRevenue', 'revenuePerShare'],
            'earnings': ['trailingEps', 'forwardEps', 'netIncomeToCommon'],
            'other_income': ['ebitda', 'freeCashflow', 'operatingCashflow'],
            
            # Balance Sheet
            'cash_debt': ['totalCash', 'totalCashPerShare', 'totalDebt'],
            'ratios': ['quickRatio', 'currentRatio', 'debtToEquity'],
            'book_value': ['bookValue', 'priceToBook']
        }

        self.translation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in translating financial analysis steps into YFinance API calls.
            
Available YFinance Metrics:
{metrics_info}

Task: Convert the given step into specific YFinance parameters.
Output should be a JSON with:
- metrics: List of exact YFinance metric names needed
- tickers: Empty list (will be filled later)
- frequency: Data frequency if needed (1d, 1wk, 1mo, 1q)
- start_date: YYYY-MM-DD format if historical data needed
- end_date: YYYY-MM-DD format if historical data needed

Example:
Input: "Get quarterly revenue for last 4 quarters"
Output: {{
    "metrics": ["totalRevenue"],
    "tickers": [],
    "frequency": "1q",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
}}"""),
            ("user", "Step to translate: {step_description}")
        ])
    def _fetch_live_data(self, tickers: List[str], metrics: List[str]) -> Dict[str, Any]:
        """Fetch live/real-time data for the given tickers."""
        try:
            data = []
            for ticker in tickers:
                stock = yf.Ticker(ticker)
                info = stock.info
                row = {"Ticker": ticker}
                for metric in metrics:
                    row[metric] = info.get(metric, None)
                data.append(row)
            return {"data": data, "error": None}
        except Exception as e:
            return {"data": None, "error": str(e)}

    def _fetch_historical_data(self, tickers: List[str], start_date: str, end_date: str, frequency: str) -> Dict[str, Any]:
        """Fetch historical data for the given tickers."""
        try:
            data = {}
            for ticker in tickers:
                stock = yf.Ticker(ticker)
                df = stock.history(start=start_date, end=end_date, interval=frequency)
                data[ticker] = df
            return {"data": data, "error": None}
        except Exception as e:
            return {"data": None, "error": str(e)}


    def _get_metrics_info(self) -> str:
        """Format available metrics info for prompt"""
        info = []
        for category, metrics in self.AVAILABLE_METRICS.items():
            info.append(f"{category.replace('_', ' ').title()}:")
            info.append(", ".join(metrics))
            info.append("")
        return "\n".join(info)

    async def _translate_step_to_request(self, step: Dict) -> DataRequest:
        """Translate a decomposition step into specific YFinance parameters"""
        try:
            # Prepare prompt with metrics info
            formatted_prompt = self.translation_prompt.format_messages(
                metrics_info=self._get_metrics_info(),
                step_description=step["description"]
            )
            
            # Get LLM response using ainvoke
            response = await self.llm.ainvoke(formatted_prompt)
            
            # Extract content from response
            content = response.content if hasattr(response, 'content') else str(response)
            print("LLM response content:", content)
            
            # Parse JSON from response
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            import json
            data = json.loads(content.strip())
            # print("Parsed data:", data)
            
            # Validate metrics against available ones
            all_available_metrics = [
                metric for metrics in self.AVAILABLE_METRICS.values()
                for metric in metrics
            ]
            data['metrics'] = [
                metric for metric in data.get('metrics', [])
                if metric in all_available_metrics
            ]
            
            # If no valid metrics found, use default
            if not data['metrics']:
                data['metrics'] = ['currentPrice']
            
            # Handle tickers
            if 'tickers' not in data:
                data['tickers'] = []
            if 'tickers' in step:
                data['tickers'].extend(step['tickers'])
            
            # Validate frequency
            if 'frequency' in data and data['frequency'] not in ['1d', '1wk', '1mo', '1q']:
                data['frequency'] = '1d'
            
            return DataRequest(**data)
            
        except Exception as e:
            print(f"Error in translation: {e}")
            print(f"Step was: {step}")
            # Return a default request with minimal data
            return DataRequest(
                metrics=['currentPrice'],
                tickers=step.get('tickers', []),
                start_date=None,
                end_date=None,
                frequency=None
            )

    def _fetch_fundamental_data(self, tickers: List[str], metrics: List[str]) -> pd.DataFrame:
        """Fetch fundamental data ensuring only valid metrics"""
        all_available_metrics = [
            metric for metrics in self.AVAILABLE_METRICS.values()
            for metric in metrics
        ]
        print("all_available_metrics", all_available_metrics)
        valid_metrics = [m for m in metrics if m in all_available_metrics]
        print("valid_metrics", valid_metrics)
        data = []
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                print("info", info)
                row = {"Ticker": ticker}
                for metric in valid_metrics:
                    row[metric] = info.get(metric, None)
                print("row", row)
                data.append(row)
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
                continue
        
        return pd.DataFrame(data)

    def _fetch_historical_data(self, tickers: List[str], start_date: str, 
                             end_date: str, interval: str) -> Dict[str, pd.DataFrame]:
        """Fetch historical data for given tickers"""
        data = {}
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                df = stock.history(start=start_date, end=end_date, interval=interval)
                data[ticker] = df
            except Exception as e:
                print(f"Error fetching historical data for {ticker}: {e}")
                continue
        return data

    def _calculate_growth_rates(self, df: pd.DataFrame, metric: str) -> pd.DataFrame:
        """Calculate YoY or QoQ growth rates for a given metric"""
        if df.empty:
            return df
        df[f"{metric}_growth"] = df[metric].pct_change(4 if 'q' in df.index else 252)
        return df

    async def execute_step(self, step: Dict) -> Dict[str, Any]:
        """Execute a single step from the query decomposition"""
        try:
            # Translate the step into specific API parameters
            print("****Translating step to request...")
            request = await self._translate_step_to_request(step)
            print("****Translated Request", request)
            # Initialize result dictionary
            result = {
                "step_number": step["step_number"],
                "description": step["description"],
                "data": None,
                "error": None
            }
            
            # Determine if historical data is needed based on start_date and end_date
            if request.start_date and request.end_date:
                print(f"Fetching historical data for {request.tickers} from {request.start_date} to {request.end_date}")
                # Convert quarterly frequency to monthly since YFinance doesn't support quarterly
                interval = '1mo' if request.frequency == '1q' else (request.frequency or '1d')
                historical_data = self._fetch_historical_data(
                    request.tickers, 
                    request.start_date, 
                    request.end_date, 
                    interval
                )
                
                # If quarterly data was requested, resample the monthly data to quarterly
                if request.frequency == '1q':
                    for ticker in historical_data:
                        historical_data[ticker] = historical_data[ticker].resample('Q').last()
                
                result["data"] = historical_data
            else:
                # Handle fundamental data for current snapshot
                print(f"Fetching fundamental data...{request.tickers} {request.metrics}")
                df = self._fetch_fundamental_data(request.tickers, request.metrics)
                result["data"] = df
             
            print("****Result", result)                   
            return result
            
        except Exception as e:
            return {
                "step_number": step["step_number"],
                "description": step["description"],
                "data": None,
                "error": str(e)
            }

    async def execute_plan(self, decomposed_query: Dict) -> List[Dict[str, Any]]:
        """Execute all steps in the decomposed query"""
        results = []
        classifier = StepClassifier()
        
        for step in decomposed_query["steps"]:
            agent_type, reason = classifier.classify_step(step)
            print(f"\nStep {step['step_number']}: {step['description']}")
            print(f"Assigned to: {agent_type.value} agent ({reason})")
            
            if agent_type == AgentType.DATA_RETRIEVAL:
                print(f"Executing step by data retrieval agent...{step}")
                result = await self.execute_step(step)
            else:
                result = {
                    "step_number": step["step_number"],
                    "description": step["description"],
                    "data": None,
                    "error": f"Step requires {agent_type.value} agent (not implemented yet)"
                }
            
            results.append(result)
            if result["error"]:
                print(f"Warning: Step {step['step_number']} failed: {result['error']}")
        
        return results