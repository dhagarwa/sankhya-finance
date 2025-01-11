from typing import Dict, List, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
from .step_classifier import StepClassifier, AgentType

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
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0
        )
        
        # Prompt to translate decomposed steps into specific API calls
        self.translation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in translating financial analysis steps into YFinance API calls.
            Convert the given step into specific YFinance metrics and parameters needed.
            
            Example Input Step:
            "Get the quarterly revenue growth rates for the last 4 quarters"
            
            Example Output:
            {{
                "metrics": ["totalRevenue"],
                "frequency": "1q",
                "start_date": "2023-01-01",
                "end_date": "2023-12-31"
            }}
            
            Return only the JSON object with the required parameters."""),
            ("user", "{step_description}")
        ])

    async def _translate_step_to_request(self, step: Dict) -> DataRequest:
        """Translate a decomposition step into specific YFinance parameters"""
        chain = self.translation_prompt | self.llm | DataRequest
        
        result = await chain.ainvoke({
            "step_description": step["description"]
        })
        
        return result

    def _fetch_fundamental_data(self, tickers: List[str], metrics: List[str]) -> pd.DataFrame:
        """Fetch fundamental data for given tickers and metrics"""
        data = []
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                row = {"Ticker": ticker}
                for metric in metrics:
                    row[metric] = info.get(metric, None)
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
            request = await self._translate_step_to_request(step)
            
            # Initialize result dictionary
            result = {
                "step_number": step["step_number"],
                "description": step["description"],
                "data": None,
                "error": None
            }
            
            # Handle fundamental data
            if not (request.start_date and request.end_date):
                df = self._fetch_fundamental_data(request.tickers, request.metrics)
                result["data"] = df
                
            # Handle historical data
            else:
                data = self._fetch_historical_data(
                    request.tickers,
                    request.start_date,
                    request.end_date,
                    request.frequency or "1d"
                )
                
                # Calculate growth rates if needed
                if any(metric.endswith('Growth') for metric in request.metrics):
                    for ticker, df in data.items():
                        base_metric = next(m for m in request.metrics if not m.endswith('Growth'))
                        data[ticker] = self._calculate_growth_rates(df, base_metric)
                
                result["data"] = data
                
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