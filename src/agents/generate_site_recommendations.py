import asyncio
import json
from pathlib import Path
from datetime import datetime
import yfinance as yf
from openai import OpenAI
import pandas as pd
from typing import Dict, List
import os

class RecommendationsGenerator:
    def __init__(self):
        self.root_dir = Path("website")
        self.client = OpenAI()
        
    def get_sp500_tickers(self) -> List[str]:
        """Get list of S&P 500 tickers"""
        sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        return sp500['Symbol'].tolist()

    def fetch_stock_data(self, ticker: str) -> Dict:
        """Fetch fundamental data for a stock"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract key metrics
            metrics = {
                'ticker': ticker,
                'pe_ratio': info.get('forwardPE', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                'revenue_growth': info.get('revenueGrowth', 'N/A'),
                'profit_margins': info.get('profitMargins', 'N/A'),
                'debt_to_equity': info.get('debtToEquity', 'N/A'),
                'current_price': info.get('currentPrice', 'N/A'),
                'target_price': info.get('targetMeanPrice', 'N/A')
            }
            return metrics
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

    async def get_gpt4_recommendation(self, metrics: Dict) -> Dict:
        """Get stock recommendation using GPT-4"""
        if not metrics:
            return {
                "ticker": metrics['ticker'],
                "recommendation": "HOLD",
                "rationale": "Insufficient data for analysis",
                "date": datetime.now().strftime("%Y-%m-%d")
            }

        prompt = f"""Analyze these stock metrics and provide a BUY, SELL, or HOLD recommendation:

        Ticker: {metrics['ticker']}
        PE Ratio: {metrics['pe_ratio']}
        Market Cap: {metrics['market_cap']}
        Dividend Yield: {metrics['dividend_yield']}
        Revenue Growth: {metrics['revenue_growth']}
        Profit Margins: {metrics['profit_margins']}
        Debt to Equity: {metrics['debt_to_equity']}
        Current Price: {metrics['current_price']}
        Target Price: {metrics['target_price']}

        Provide only BUY, SELL, or HOLD followed by a brief one-sentence rationale.
        Format: RECOMMENDATION: rationale
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=100
            )
            
            content = response.choices[0].message.content
            parts = content.split(":", 1)
            recommendation = "HOLD"
            rationale = "Insufficient data for analysis"
            
            if len(parts) == 2:
                recommendation = parts[0].strip().upper()
                rationale = parts[1].strip()
                
                # Ensure recommendation is valid
                if recommendation not in ["BUY", "SELL", "HOLD"]:
                    recommendation = "HOLD"
            
            return {
                "ticker": metrics['ticker'],
                "recommendation": recommendation,
                "rationale": rationale,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            
        except Exception as e:
            print(f"Error getting recommendation for {metrics['ticker']}: {e}")
            return {
                "ticker": metrics['ticker'],
                "recommendation": "HOLD",
                "rationale": "Error in analysis",
                "date": datetime.now().strftime("%Y-%m-%d")
            }

    async def update_recommendations(self):
        """Update stock recommendations"""
        print("\nUpdating stock recommendations...")
        
        # Get S&P 500 tickers
        tickers = self.get_sp500_tickers()
        
        # Fetch data and get recommendations
        recommendations = []
        for ticker in tickers:
            print(f"Analyzing {ticker}...")
            metrics = self.fetch_stock_data(ticker)
            if metrics:
                rec = await self.get_gpt4_recommendation(metrics)
                recommendations.append(rec)
                # Small delay to respect API rate limits
                await asyncio.sleep(1)
        
        # Save recommendations
        data_dir = self.root_dir / "src/data"
        data_dir.mkdir(exist_ok=True)
        
        with open(data_dir / "recommendations.json", "w") as f:
            json.dump(recommendations, f, indent=2)
        
        print(f"\nRecommendations updated successfully at: {data_dir / 'recommendations.json'}")

if __name__ == "__main__":
    generator = RecommendationsGenerator()
    asyncio.run(generator.update_recommendations()) 