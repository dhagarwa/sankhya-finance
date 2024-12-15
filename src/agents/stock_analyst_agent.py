from typing import Dict, List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
import pandas as pd
from datetime import datetime
import os
from rich.console import Console
from rich.table import Table
import asyncio
from yfinance_metrics import get_sp500_tickers, fetch_fundamentals
import time

class StockRecommendation(BaseModel):
    """Schema for stock recommendations"""
    ticker: str = Field(description="Stock ticker symbol")
    recommendation: str = Field(description="Buy, Sell, or Hold recommendation")
    confidence: float = Field(description="Confidence score between 0 and 1")
    rationale: str = Field(description="Brief rationale for the recommendation")

class StockAnalystAgent:
    """
    Agent that provides stock recommendations using Gemini Flash API based on fundamental analysis
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0
        )
        
        # Initialize rate limiting parameters
        self.rate_limit = 15  # requests per minute
        self.last_request_time = time.time()
        self.request_count = 0
        
        self.recommendation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert stock analyst. Analyze the given stock data and provide a recommendation.
            Consider these key metrics:
            1. Valuation: PE ratio, PB ratio, Price/Sales
            2. Growth: Revenue growth, Earnings growth
            3. Profitability: Margins, ROE, ROA
            4. Market Position: Market cap, Industry rank
            5. Risk Metrics: Beta, Debt/Equity
            
            Respond in exactly this format:
            BUY|0.95|Strong growth and reasonable valuation
            or
            SELL|0.80|Declining margins and high valuation
            or
            HOLD|0.70|Fair valuation but uncertain growth
            
            Only these three words (BUY/SELL/HOLD) are allowed."""),
            ("user", """Stock: {ticker}
            Metrics:
            {metrics}""")
        ])

    async def _enforce_rate_limit(self):
        """Enforce rate limiting for API calls"""
        current_time = time.time()
        if current_time - self.last_request_time < 60:  # within the same minute
            if self.request_count >= self.rate_limit:
                wait_time = 60 - (current_time - self.last_request_time)
                print(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
                await asyncio.sleep(wait_time)
                self.request_count = 0
                self.last_request_time = time.time()
        else:
            # Reset counters for new minute
            self.request_count = 0
            self.last_request_time = current_time
        
        self.request_count += 1

    async def get_recommendation(self, ticker: str, metrics: Dict) -> StockRecommendation:
        """Get recommendation for a single stock"""
        try:
            await self._enforce_rate_limit()
            
            # Format metrics for the prompt
            metrics_str = "\n".join([f"{k}: {v}" for k, v in metrics.items()])
            
            # Get recommendation from Gemini
            chain = self.recommendation_prompt | self.llm
            response = await chain.ainvoke({
                "ticker": ticker,
                "metrics": metrics_str
            })
            
            # Parse response
            rec, conf, rationale = response.content.strip().split("|")
            
            return StockRecommendation(
                ticker=ticker,
                recommendation=rec.strip().upper(),
                confidence=float(conf.strip()),
                rationale=rationale.strip()
            )
            
        except Exception as e:
            print(f"Error getting recommendation for {ticker}: {e}")
            return None

    async def analyze_sp500(self) -> pd.DataFrame:
        """Analyze all S&P 500 stocks with rate limiting"""
        # Get S&P 500 tickers
        tickers = get_sp500_tickers()
        # Fetch fundamentals for all stocks
        fundamentals_df = fetch_fundamentals(tickers)
        
        # Get recommendations with rate limiting
        recommendations = []
        for _, row in fundamentals_df.iterrows():
            rec = await self.get_recommendation(row['Ticker'], row.to_dict())
            if rec:
                recommendations.append(rec)
        
        # Convert to DataFrame
        df = pd.DataFrame([r.dict() for r in recommendations])
        df['date'] = datetime.now().date()
        
        return df

    def display_recommendations(self, df: pd.DataFrame):
        """Display recommendations in a rich formatted table"""
        console = Console()
        
        table = Table(
            title=f" Sankhya AI Stock Recommendations - {datetime.now().date()}",
            show_header=True,
            header_style="bold magenta",
            border_style="blue"
        )
        
        table.add_column("Ticker", style="cyan", justify="center")
        table.add_column("Signal", style="bold", justify="center")
        table.add_column("Confidence", justify="right")
        table.add_column("Analysis", style="italic")
        
        for _, row in df.iterrows():
            rec_style = {
                "BUY": "green",
                "SELL": "red",
                "HOLD": "yellow"
            }.get(row['recommendation'], "white")
            
            confidence_str = f"{row['confidence']*100:.1f}%"
            
            table.add_row(
                f"[bold]{row['ticker']}[/bold]",
                f"[{rec_style}]{row['recommendation']}[/{rec_style}]",
                confidence_str,
                row['rationale']
            )
        
        console.print("\n")
        console.rule("[bold blue]Stock Analysis Report[/bold blue]")
        console.print(table)
        console.rule("[dim]Generated by Sankhya AI[/dim]") 