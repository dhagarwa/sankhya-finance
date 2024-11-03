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

    async def fetch_stock_prices(self, ticker: str, target_date: str, window_days: int = 5) -> Dict[str, Any]:
        """
        Fetch stock price for a specific date or closest business day.
        
        Args:
            ticker: Stock symbol
            target_date: Target date in 'YYYY-MM-DD' format
            window_days: Number of days to look before and after target date (default 5)
        
        Returns:
            Dictionary containing the price data for closest available date
        """
        try:
            # Convert target_date to datetime
            target_dt = datetime.strptime(target_date, '%Y-%m-%d')
            
            # Calculate window start and end dates
            start_date = (target_dt - timedelta(days=window_days)).strftime('%Y-%m-%d')
            end_date = (target_dt + timedelta(days=window_days)).strftime('%Y-%m-%d')
            
            # Build endpoint URL for daily bars
            endpoint = f"{self.base_url}/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}"
            
            params = {
                "apiKey": self.api_key,
                "adjusted": "true",
                "sort": "asc"  # Sort by date ascending
            }
            
            logger.info(f"Fetching prices for {ticker} between {start_date} and {end_date}")
            
            async with self.session.get(endpoint, params=params) as response:
                if response.status != 200:
                    logger.error(f"Error fetching price data for {ticker}: {response.status}")
                    return None
                
                data = await response.json()
                
                if data.get('status') == 'ERROR':
                    logger.error(f"API error for {ticker}: {data.get('error')}")
                    return None
                
                if not data.get('results'):
                    logger.warning(f"No price data found for {ticker} around {target_date}")
                    return None
                
                # Find the closest date to target_date
                target_timestamp = target_dt.timestamp() * 1000  # Convert to milliseconds
                closest_result = min(
                    data['results'],
                    key=lambda x: abs(x['t'] - target_timestamp)
                )
                
                # Create a clean response with just the closest day's data
                response_data = {
                    'status': 'OK',
                    'ticker': ticker,
                    'target_date': target_date,
                    'actual_date': datetime.fromtimestamp(closest_result['t']/1000).strftime('%Y-%m-%d'),
                    'results': [closest_result]
                }
                
                logger.info(
                    f"Found price for {ticker} on {response_data['actual_date']} "
                    f"(target: {target_date}): ${closest_result['c']}"
                )
                
                return response_data
                
        except Exception as e:
            logger.error(f"Error fetching price data for {ticker} on {target_date}: {str(e)}")
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
        
        # Change ticker to "SaaS Trifecta"
        combined_df['ticker'] = 'SaaS Trifecta'
        # Calculate growth rates
        combined_df['Revenue YoY Growth (%)'] = combined_df[revenue_col].pct_change(-4) * 100
        combined_df['Income YoY Growth (%)'] = combined_df[income_col].pct_change(-4) * 100
        combined_df['Cash Flow YoY Growth (%)'] = combined_df[cashflow_col].pct_change(-4) * 100
        
        # Round numeric columns
        numeric_columns = combined_df.select_dtypes(include=['float64']).columns
        combined_df[numeric_columns] = combined_df[numeric_columns].round(2)
        
        print("\nCombined SaaS Companies Metrics:")
        print(combined_df.to_string())
        # import pdb; pdb.set_trace()
        return company_dfs, combined_df
        
    except Exception as e:
        print(f"Error in SaaS analysis: {str(e)}")
        # Print actual column names when error occurs
        for ticker, df in company_dfs.items():
            print(f"\n{ticker} DataFrame columns:")
            print(df.columns.tolist())
        raise



async def fetch_saas_trifecta_history() -> Dict[str, pd.DataFrame]:
    """
    Fetches quarterly price and market cap data for ADBE, CRM, and NOW over the last 5 years.
    Returns a dictionary of DataFrames, one for each company.
    """
    try:
        saas_tickers = ["ADBE", "CRM", "NOW"]
        company_data = {}
        
        # Generate quarterly dates for last 5 years
        end_date = datetime.now()
        dates = []
        for i in range(20):  # 20 quarters = 5 years
            quarter_end = end_date - relativedelta(months=3*i)
            # Use the 15th of the last month of each quarter for consistency
            quarter_end = quarter_end.replace(day=15)
            dates.append(quarter_end.strftime('%Y-%m-%d'))
        
        dates.reverse()  # Sort chronologically
        
        service = PolygonFinancialService()
        async with service:
            for ticker in saas_tickers:
                quarterly_data = []
                
                print(f"\nFetching data for {ticker}")
                print("=" * 50)
                
                for date in dates:
                    print(f"Processing date: {date}")
                    
                    # Fetch price data
                    price_data = await service.fetch_stock_prices(ticker, date)
                    
                    if price_data and price_data.get('results'):
                        result = price_data['results'][0]
                        close_price = result['c']
                        
                        # Fetch financial data for shares outstanding
                        financial_data = await service.fetch_financial_data(ticker)
                        shares_outstanding = None
                        
                        if financial_data and financial_data.get('results'):
                            # Get the most recent financial data before this date
                            try:
                                relevant_data = next(
                                    (data for data in financial_data['results'] 
                                    if data['start_date'] <= date),
                                    None
                                )

                                if relevant_data and 'financials' in relevant_data:
                                    income_statement = relevant_data['financials'].get('income_statement', {})
                                    if 'basic_average_shares' in income_statement:
                                        shares_outstanding = income_statement['basic_average_shares']['value']
                                        if shares_outstanding is None or shares_outstanding <= 0:
                                            import pdb; pdb.set_trace()
                                        
                                else:
                                    raise Exception(f"No shares outstanding data found for {ticker}")
                            except Exception as e:
                                print(f"Error fetching financial data for {ticker}: {str(e)}")
                                import pdb; pdb.set_trace()
                                continue
                            
                        quarter_info = {
                            'date': date,
                            'quarter': f"Q{(datetime.strptime(date, '%Y-%m-%d').month-1)//3 + 1} "
                                     f"{datetime.strptime(date, '%Y-%m-%d').year}",
                            'close_price': close_price,
                            'actual_date': price_data['actual_date'],
                            'volume': result['v'],
                            'shares_outstanding': shares_outstanding,
                            'market_cap': shares_outstanding * close_price if shares_outstanding else None
                        }
                        
                        print(f"Close Price: ${close_price:,.2f}")
                        print(f"Market Cap: ${quarter_info['market_cap']:,.2f}" if quarter_info['market_cap'] else "Market Cap: N/A")
                        print("-" * 30)
                        
                        quarterly_data.append(quarter_info)
                
                # Create DataFrame for this company
                df = pd.DataFrame(quarterly_data)
                
                # Calculate quarter-over-quarter and year-over-year returns
                df['qoq_return'] = df['close_price'].pct_change() * 100
                df['yoy_return'] = df['close_price'].pct_change(periods=4) * 100
                
                # Format market cap in billions
                if 'market_cap' in df.columns:
                    df['market_cap_billions'] = df['market_cap'] / 1_000_000_000
                
                # Round numeric columns
                numeric_cols = df.select_dtypes(include=['float64']).columns
                df[numeric_cols] = df[numeric_cols].round(2)
                
                company_data[ticker] = df
                
                # Export individual company data
                os.makedirs('exports', exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'exports/{ticker}_historical_data_{timestamp}.csv'
                df.to_csv(filename, index=False)
                print(f"\nData exported to {filename}")
        
        return company_data
        
    except Exception as e:
        logger.error(f"Error fetching SaaS Trifecta history: {str(e)}")
        raise



def create_saas_trifecta_index(company_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Creates a market cap weighted index from individual company data.
    
    Args:
        company_data: Dictionary with company tickers as keys and DataFrames as values
    
    Returns:
        DataFrame with market cap weighted index
    """
    try:
        # Create a new DataFrame with just the date column from first company
        first_company_df = next(iter(company_data.values()))
        index_df = pd.DataFrame({
            'date': first_company_df['date'],
            'quarter': first_company_df['quarter']
        })
        
        # For each date, calculate total market cap and weighted prices
        for date in index_df['date']:
            total_market_cap = 0
            weighted_price = 0
            
            # First calculate total market cap for this date
            for ticker, df in company_data.items():
                date_data = df[df['date'] == date].iloc[0]
                if pd.notna(date_data['market_cap']) and date_data['market_cap'] > 0:
                    total_market_cap += date_data['market_cap']
            
            # Then calculate weighted price contributions
            for ticker, df in company_data.items():
                date_data = df[df['date'] == date].iloc[0]
                if pd.notna(date_data['market_cap']) and date_data['market_cap'] > 0:
                    weight = date_data['market_cap'] / total_market_cap
                    weighted_price += date_data['close_price'] * weight
                    
                    # Store individual company data
                    index_df.loc[index_df['date'] == date, f'{ticker}_price'] = date_data['close_price']
                    index_df.loc[index_df['date'] == date, f'{ticker}_weight'] = weight * 100  # as percentage
                    index_df.loc[index_df['date'] == date, f'{ticker}_market_cap_B'] = date_data['market_cap'] / 1e9
            
            index_df.loc[index_df['date'] == date, 'weighted_price'] = weighted_price
            index_df.loc[index_df['date'] == date, 'total_market_cap_B'] = total_market_cap / 1e9
        
        # Calculate returns
        index_df['qoq_return'] = index_df['weighted_price'].pct_change() * 100
        index_df['yoy_return'] = index_df['weighted_price'].pct_change(periods=4) * 100
        
        # Round numeric columns
        numeric_cols = index_df.select_dtypes(include=['float64']).columns
        index_df[numeric_cols] = index_df[numeric_cols].round(2)
        
        # Export to CSV
        os.makedirs('exports', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'exports/saas_trifecta_index_{timestamp}.csv'
        index_df.to_csv(filename, index=False)
        print(f"\nIndex data exported to {filename}")
        
        return index_df
        
    except Exception as e:
        logger.error(f"Error creating SaaS Trifecta index: {str(e)}")
        raise




async def main():
    try:
        # Single stock analysis
        df_aapl = await analyze_quarterly_metrics("ADBE")
        print(df_aapl)
            
    except Exception as e:
        print(f"Main execution error: {str(e)}")
        raise

async def test_stock_price_fetch():
    """Simple test function to verify stock price fetching."""
    try:
        service = PolygonFinancialService()
        async with service:
            # Test cases
            test_cases = [
                ("AAPL", "2024-01-15"),  # Recent date
                ("MSFT", "2023-12-25"),  # Holiday
                ("GOOGL", "2024-01-13"), # Weekend
            ]
            
            print("\nTesting stock price fetching:")
            print("=" * 50)
            
            for ticker, date in test_cases:
                print(f"\nFetching {ticker} for target date: {date}")
                price_data = await service.fetch_stock_prices(ticker, date)
                print(price_data)
                if price_data and price_data.get('results'):
                    result = price_data['results'][0]
                    print(f"Target date: {price_data['target_date']}")
                    print(f"Actual date: {price_data['actual_date']}")
                    print(f"Close price: ${result['c']:,.2f}")
                    print(f"Volume: {result['v']:,}")
                    print("-" * 30)
                else:
                    print(f"Failed to fetch data for {ticker}")
                    
    except Exception as e:
        print(f"Error in test function: {str(e)}")
        raise






if __name__ == "__main__":
    # asyncio.run(main())
    # TESTING analysze SaaS companies fundamentals
    # asyncio.run(analyze_saas_companies())
    
    # TESTING stock price fetching
    # asyncio.run(test_stock_price_fetch())
    
    company_data = asyncio.run(fetch_saas_trifecta_history())
    index_df = create_saas_trifecta_index(company_data)
    import pdb; pdb.set_trace()
