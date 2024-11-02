import os
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import aiohttp
import asyncio
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnvironmentManager:
    @staticmethod
    def load_environment() -> str:
        env_path = Path('.') / '.env'
        if not env_path.exists():
            raise FileNotFoundError(
                "'.env' file not found. Please create one using '.env.template' as a reference."
            )
        
        load_dotenv()
        api_key = os.getenv('POLYGON_API_KEY')
        if not api_key:
            raise ValueError(
                "POLYGON_API_KEY not found in environment variables. "
                "Please add it to your .env file."
            )
            
        return api_key

class PolygonFinancialService:
    def __init__(self):
        self.api_key = EnvironmentManager.load_environment()
        self.base_url = "https://api.polygon.io"
        self.session = None
        logger.info("PolygonFinancialService initialized successfully")

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_financial_data(self, ticker: str, timespan: str = "quarterly") -> Dict[str, Any]:
        """Fetch financial statements data from Polygon."""
        endpoint = f"{self.base_url}/vX/reference/financials"
        params = {
            "ticker": ticker,
            "timeframe": timespan,
            "apiKey": self.api_key,
            "limit": 20,  # Last 5 years of quarterly data
            "sort": "period_of_report_date"  # Sort by report date
        }
        
        try:
            async with self.session.get(endpoint, params=params) as response:
                if response.status != 200:
                    logger.error(f"Error fetching financial data for {ticker}: {response.status}")
                    return None
                data = await response.json()
                logger.info(f"Successfully fetched financial data for {ticker}")
                # Log the first result structure for debugging
                if data.get('results') and len(data['results']) > 0:
                    logger.debug(f"Sample data structure: {data['results'][0].keys()}")
                return data
        except Exception as e:
            logger.error(f"Error fetching financial data for {ticker}: {str(e)}")
            return None

    async def fetch_stock_prices(self, ticker: str, from_date: str, to_date: str) -> Dict[str, Any]:
        """Fetch daily adjusted close prices."""
        endpoint = f"{self.base_url}/v2/aggs/ticker/{ticker}/range/1/day/{from_date}/{to_date}"
        params = {"apiKey": self.api_key, "adjusted": "true"}
        
        try:
            async with self.session.get(endpoint, params=params) as response:
                if response.status != 200:
                    logger.error(f"Error fetching price data for {ticker}: {response.status}")
                    return None
                data = await response.json()
                return data
        except Exception as e:
            logger.error(f"Error fetching price data for {ticker}: {str(e)}")
            return None

    def calculate_growth_metrics(self, financial_data: Dict[str, Any]) -> Dict[str, List[float]]:
        """Calculate year-over-year growth metrics."""
        if not financial_data or 'results' not in financial_data or not financial_data['results']:
            logger.warning("No financial data available for growth metrics calculation")
            return {
                'dates': [],
                'revenue_growth': [],
                'fcf_growth': []
            }

        results = {
            'dates': [],
            'revenue_growth': [],
            'fcf_growth': []
        }
        
        try:
            # Debug log the structure of first few results
            logger.info(f"Number of results: {len(financial_data['results'])}")
            logger.info(f"Keys in first result: {financial_data['results'][0].keys()}")
            
            # Filter out entries without filing_date
            valid_statements = [
                statement for statement in financial_data['results']
                if 'filing_date' in statement
            ]
            
            if not valid_statements:
                logger.error("No valid statements with filing_date found")
                return results
                
            # Sort the valid statements
            statements = sorted(
                valid_statements,
                key=lambda x: x['filing_date'],
                reverse=True
            )
            
            # Calculate YoY growth rates
            for i in range(len(statements) - 4):  # Need previous year's quarter for YoY
                try:
                    current = statements[i]
                    prev_year = statements[i + 4]
                    
                    # Log the dates we're comparing
                    logger.debug(f"Comparing {current['filing_date']} with {prev_year['filing_date']}")
                    
                    # Revenue growth
                    try:
                        current_revenue = float(current['financials']['income_statement']['revenues']['value'])
                        prev_revenue = float(prev_year['financials']['income_statement']['revenues']['value'])
                        revenue_growth = ((current_revenue - prev_revenue) / prev_revenue) * 100 if prev_revenue != 0 else 0
                    except (KeyError, TypeError, ValueError) as e:
                        logger.warning(f"Error calculating revenue growth: {str(e)}")
                        revenue_growth = 0
                    
                    # Free Cash Flow growth
                    try:
                        current_operating_cf = float(current['financials']['cash_flow_statement']['net_cash_flow_from_operating_activities']['value'])
                        current_capex = float(current['financials']['cash_flow_statement']['capital_expenditure']['value'])
                        prev_operating_cf = float(prev_year['financials']['cash_flow_statement']['net_cash_flow_from_operating_activities']['value'])
                        prev_capex = float(prev_year['financials']['cash_flow_statement']['capital_expenditure']['value'])
                        
                        current_fcf = current_operating_cf - current_capex
                        prev_fcf = prev_operating_cf - prev_capex
                        
                        fcf_growth = ((current_fcf - prev_fcf) / abs(prev_fcf)) * 100 if prev_fcf != 0 else 0
                    except (KeyError, TypeError, ValueError) as e:
                        logger.warning(f"Error calculating FCF growth: {str(e)}")
                        fcf_growth = 0
                    
                    results['dates'].append(current['filing_date'])
                    results['revenue_growth'].append(round(revenue_growth, 2))
                    results['fcf_growth'].append(round(fcf_growth, 2))
                    
                except Exception as e:
                    logger.error(f"Error processing statement: {str(e)}")
                    continue
        
        except Exception as e:
            logger.error(f"Error calculating growth metrics: {str(e)}")
            logger.error(f"First result structure: {financial_data['results'][0] if financial_data.get('results') else 'No results'}")
            
        return results

    def calculate_price_returns(self, price_data: Dict[str, Any], benchmark_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate total return and relative performance vs benchmarks."""
        try:
            if not price_data or not price_data.get('results') or not benchmark_data or not benchmark_data.get('results'):
                return {
                    'total_return': 0,
                    'relative_return': 0
                }
                
            stock_return = (
                price_data['results'][-1]['c'] / price_data['results'][0]['c'] - 1
            ) * 100
            
            benchmark_return = (
                benchmark_data['results'][-1]['c'] / benchmark_data['results'][0]['c'] - 1
            ) * 100
            
            return {
                'total_return': round(stock_return, 2),
                'relative_return': round(stock_return - benchmark_return, 2)
            }
        except Exception as e:
            logger.error(f"Error calculating price returns: {str(e)}")
            return {
                'total_return': 0,
                'relative_return': 0
            }
            
            

    async def fetch_and_debug_financial_data(self, ticker: str) -> None:
        """Debug function to examine the structure of financial data."""
        try:
            financial_data = await self.fetch_financial_data(ticker)
            if financial_data and 'results' in financial_data and financial_data['results']:
                logger.info(f"\nDebug info for {ticker}:")
                logger.info(f"Number of results: {len(financial_data['results'])}")
                logger.info(f"Keys in first result: {list(financial_data['results'][0].keys())}")
                logger.info(f"Filing date value: {financial_data['results'][0].get('filing_date', 'NOT FOUND')}")
                logger.info(f"Start period: {financial_data['results'][0].get('start_date', 'NOT FOUND')}")
                logger.info(f"End period: {financial_data['results'][0].get('end_date', 'NOT FOUND')}")
                logger.info(f"Report period: {financial_data['results'][0].get('period_of_report_date', 'NOT FOUND')}")
            else:
                logger.error(f"No valid data found for {ticker}")
        except Exception as e:
            logger.error(f"Error in debug function: {str(e)}")


class StockAnalyzer:
    def __init__(self):
        self.service = PolygonFinancialService()

    async def analyze_stock_bucket(self, tickers: List[str]) -> Dict[str, Any]:
        """Analyze a group of stocks and compare their metrics."""
        five_years_ago = (datetime.now() - relativedelta(years=5)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')
        
        results = {}
        
        async with self.service as service:
            for ticker in tickers:
                try:
                    logger.info(f"Analyzing {ticker}...")
                    
                    # Fetch all required data
                    financial_data = await service.fetch_financial_data(ticker)
                    if financial_data:
                        logger.debug(f"Financial data keys: {financial_data.keys()}")
                    
                    stock_prices = await service.fetch_stock_prices(ticker, five_years_ago, today)
                    spy_prices = await service.fetch_stock_prices("SPY", five_years_ago, today)
                    qqq_prices = await service.fetch_stock_prices("QQQ", five_years_ago, today)
                    
                    if not all([financial_data, stock_prices, spy_prices, qqq_prices]):
                        logger.warning(f"Incomplete data for {ticker}, skipping...")
                        continue
                    
                    # Calculate metrics
                    growth_metrics = service.calculate_growth_metrics(financial_data)
                    spy_performance = service.calculate_price_returns(stock_prices, spy_prices)
                    qqq_performance = service.calculate_price_returns(stock_prices, qqq_prices)
                    
                    results[ticker] = {
                        'growth_metrics': growth_metrics,
                        'spy_performance': spy_performance,
                        'qqq_performance': qqq_performance
                    }
                    
                except Exception as e:
                    logger.error(f"Error analyzing {ticker}: {str(e)}")
                    continue
        
        return results



def extract_quarterly_metrics(financial_data: Dict[str, Any], ticker: str) -> pd.DataFrame:
    """
    Extract quarterly revenue and cash flow metrics from financial data.
    """
    if not financial_data or 'results' not in financial_data:
        print(f"No financial data available for {ticker}")
        return pd.DataFrame()

    quarterly_data = []
    
    for statement in financial_data['results']:
        try:
            fiscal_year = int(statement.get('fiscal_year', 0))
            fiscal_quarter = int(statement.get('fiscal_period', '').replace('Q', ''))
            
            # Create a sortable numerical key
            sort_key = fiscal_year * 10 + fiscal_quarter
            # Extract basic quarterly information
            quarter_info = {
                'sort_key': sort_key,
                'ticker': ticker,
                'quarter': f"Q{statement.get('fiscal_period', '').replace('Q', '')} {statement.get('fiscal_year', '')}",
                'date': statement.get('period_of_report_date', ''),
                
                # Revenue
                'revenue': float(statement['financials']['income_statement']['revenues']['value']),
                
                # Cash Flow Components
                'operating_cash_flow': float(statement['financials']['cash_flow_statement']['net_cash_flow_from_operating_activities']['value']),
                'investing_cash_flow': float(statement['financials']['cash_flow_statement']['net_cash_flow_from_investing_activities']['value']),
                'financing_cash_flow': float(statement['financials']['cash_flow_statement']['net_cash_flow_from_financing_activities']['value']),
                
                # Operating Metrics
                'operating_income': float(statement['financials']['income_statement']['operating_income_loss']['value']),
                'net_income': float(statement['financials']['income_statement']['net_income_loss']['value']),
                'gross_profit': float(statement['financials']['income_statement']['gross_profit']['value'])
            }
            
            quarterly_data.append(quarter_info)
            
        except Exception as e:
            print(f"Warning: Error processing quarter data: {str(e)}")
            continue
    
    # Sort quarterly_data list before creating DataFrame
    quarterly_data = sorted(quarterly_data, key=lambda x: x['sort_key'], reverse=True)
    
    # Remove sort_key before creating DataFrame
    for item in quarterly_data:
        item.pop('sort_key')
        
    # Convert to DataFrame
    df = pd.DataFrame(quarterly_data)
    
    if df.empty:
        return df
    
    # Reset index
    df = df.reset_index(drop=True)
    
    
    # Calculate growth rates
    df['revenue_qoq_growth'] = df['revenue'].pct_change(-1) * 100
    df['revenue_yoy_growth'] = df['revenue'].pct_change(-4) * 100
    df['operating_income_yoy_growth'] = df['operating_income'].pct_change(-4) * 100
    df['operating_cash_flow_yoy_growth'] = df['operating_cash_flow'].pct_change(-4) * 100
    # Format numbers (in millions for better readability)
    for col in ['revenue', 'operating_cash_flow', 'investing_cash_flow', 'financing_cash_flow', 
                'operating_income', 'net_income', 'gross_profit']:
        df[col] = df[col] / 1_000_000  # Convert to millions
        df[col] = df[col].round(2)
    
    # Format growth rates
    for col in ['revenue_qoq_growth', 'revenue_yoy_growth', 'operating_income_yoy_growth']:
        df[col] = df[col].round(1)
    
    # Add column labels
    df = df.rename(columns={
        'revenue': 'Revenue ($M)',
        'operating_cash_flow': 'Operating Cash Flow ($M)',
        'investing_cash_flow': 'Investing Cash Flow ($M)',
        'financing_cash_flow': 'Financing Cash Flow ($M)',
        'operating_income': 'Operating Income ($M)',
        'net_income': 'Net Income ($M)',
        'gross_profit': 'Gross Profit ($M)',
        'revenue_qoq_growth': 'Revenue QoQ Growth (%)',
        'revenue_yoy_growth': 'Revenue YoY Growth (%)',
        'operating_income_yoy_growth': 'Operating Income YoY Growth (%)'
    })
    
    return df


async def analyze_quarterly_metrics(ticker: str) -> pd.DataFrame:
    """
    Fetch and analyze quarterly metrics for a single ticker.
    """
    try:
        service = PolygonFinancialService()
        async with service:
            financial_data = await service.fetch_financial_data(ticker)
            
            if financial_data:
                df = extract_quarterly_metrics(financial_data, ticker)
                
                if not df.empty:
                    print(f"\nQuarterly metrics for {ticker}:")
                    print(df.to_string(index=False))
                    
                    # Optional: Export to CSV
                    os.makedirs('exports', exist_ok=True)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f'exports/{ticker}_quarterly_metrics_{timestamp}.csv'
                    df.to_csv(filename, index=False)
                    print(f"\nData exported to {filename}")
                    
                return df
            else:
                print(f"No financial data available for {ticker}")
                return pd.DataFrame()
                
    except Exception as e:
        print(f"Error processing {ticker}: {str(e)}")
        return pd.DataFrame()

# async def main():
#     try:
#         analyzer = StockAnalyzer()
#         # Test with a single stock first
#         test_ticker = "AAPL"
#         logger.info(f"\nDebug: Fetching data for {test_ticker}")
#         await analyzer.service.fetch_and_debug_financial_data(test_ticker)
        
#         # Example stock bucket
#         tech_stocks = ["AAPL", "MSFT", "GOOGL", "NVDA", "META"]
        
#         # Analyze stocks
#         results = await analyzer.analyze_stock_bucket(tech_stocks)
        
#         # Convert results to DataFrame for easier visualization
#         data = []
#         for ticker, metrics in results.items():
#             try:
#                 avg_revenue_growth = (
#                     sum(metrics['growth_metrics']['revenue_growth']) / 
#                     len(metrics['growth_metrics']['revenue_growth'])
#                 ) if metrics['growth_metrics']['revenue_growth'] else 0
                
#                 avg_fcf_growth = (
#                     sum(metrics['growth_metrics']['fcf_growth']) / 
#                     len(metrics['growth_metrics']['fcf_growth'])
#                 ) if metrics['growth_metrics']['fcf_growth'] else 0
                
#                 data.append({
#                     'ticker': ticker,
#                     'avg_revenue_growth': round(avg_revenue_growth, 2),
#                     'avg_fcf_growth': round(avg_fcf_growth, 2),
#                     'vs_spy': metrics['spy_performance']['relative_return'],
#                     'vs_qqq': metrics['qqq_performance']['relative_return']
#                 })
#             except Exception as e:
#                 logger.error(f"Error processing results for {ticker}: {str(e)}")
#                 continue
        
#         df = pd.DataFrame(data)
#         print("\nAnalysis Results:")
#         print(df.to_string())
        
#     except Exception as e:
#         logger.error(f"Main execution error: {str(e)}")
#         raise


async def analyze_saas_companies():
    try:
        saas_tickers = ["ADBE", "CRM", "NOW"]
        company_dfs = {}
        
        print("\nAnalyzing individual companies...")
        for ticker in saas_tickers:
            print(f"\nAnalyzing {ticker}...")
            df = await analyze_quarterly_metrics(ticker)
            if not df.empty:
                company_dfs[ticker] = df
                print(f"\n{ticker} Column Names:")  # Debug print
                print(df.columns.tolist())  # Debug print
        
        # import pdb; pdb.set_trace()
        # Get the first DataFrame's structure
        first_df = next(iter(company_dfs.values()))
        print("\nFirst DataFrame columns:")  # Debug print
        print(first_df.columns.tolist())  # Debug print
        combined_df = first_df.copy()
        
        # Map column names - adjust these based on the debug output
        revenue_col = 'Revenue ($M)'  # Verify this exists
        income_col = 'Operating Income ($M)'  # This might be the actual name
        cashflow_col = 'Operating Cash Flow ($M)'  # Verify this exists
        
        # Initialize sum columns
        combined_df[revenue_col] = 0
        combined_df[income_col] = 0
        combined_df[cashflow_col] = 0
        
        # Add values from each company
        for df in company_dfs.values():
            combined_df[revenue_col] += df[revenue_col]
            combined_df[income_col] += df[income_col]
            combined_df[cashflow_col] += df[cashflow_col]
        
        # Calculate growth rates
        combined_df['Revenue YoY Growth (%)'] = combined_df[revenue_col].pct_change(-4) * 100
        combined_df['Income YoY Growth (%)'] = combined_df[income_col].pct_change(-4) * 100
        combined_df['Cash Flow YoY Growth (%)'] = combined_df[cashflow_col].pct_change(-4) * 100
        
        # Round numeric columns
        numeric_columns = combined_df.select_dtypes(include=['float64']).columns
        combined_df[numeric_columns] = combined_df[numeric_columns].round(2)
        
        print("\nCombined SaaS Companies Metrics:")
        # print(combined_df.to_string())
        import pdb; pdb.set_trace()
        return company_dfs, combined_df
        
    except Exception as e:
        print(f"Error in SaaS analysis: {str(e)}")
        # Print actual column names when error occurs
        for ticker, df in company_dfs.items():
            print(f"\n{ticker} DataFrame columns:")
            print(df.columns.tolist())
        raise


async def main():
    try:
        # Single stock analysis
        df_aapl = await analyze_quarterly_metrics("ADBE")
        print(df_aapl)
            
    except Exception as e:
        print(f"Main execution error: {str(e)}")
        raise

if __name__ == "__main__":
    # asyncio.run(main())
    asyncio.run(analyze_saas_companies())