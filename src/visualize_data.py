import pandas as pd
from typing import Dict, Any
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
import asyncio
from src.bucket_fundamentals import PolygonFinancialService

def export_financial_data_to_csv(financial_data: Dict[str, Any], ticker: str) -> str:
    """
    Export all raw financial data to CSV format, organized by quarters.
    
    Args:
        financial_data: Dictionary containing financial data from Polygon API
        ticker: Stock ticker symbol
    
    Returns:
        str: Path to the saved CSV file
    """
    if not financial_data or 'results' not in financial_data:
        raise ValueError("No financial data available for export")

    raw_data = []
    
    # First, flatten the nested dictionary structure
    def flatten_dict(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    # Process each quarterly statement
    for statement in financial_data['results']:
        try:
            # Extract quarter information
            quarter = {
                'ticker': ticker,
                'quarter': f"Q{statement.get('fiscal_period', '').replace('Q', '')} {statement.get('fiscal_year', '')}",
                'period_of_report_date': statement.get('period_of_report_date', ''),
                'filing_date': statement.get('filing_date', ''),
                'start_date': statement.get('start_date', ''),
                'end_date': statement.get('end_date', ''),
            }
            
            # Flatten the financials data
            if 'financials' in statement:
                flattened_financials = flatten_dict(statement['financials'])
                quarter.update(flattened_financials)
            
            # Add any other top-level keys (excluding 'financials' which we've already processed)
            for key, value in statement.items():
                if key != 'financials':
                    if isinstance(value, dict):
                        flattened = flatten_dict({key: value})
                        quarter.update(flattened)
                    else:
                        quarter[key] = value
            
            raw_data.append(quarter)
            
        except Exception as e:
            print(f"Warning: Error processing statement: {str(e)}")
            continue

    # Convert to DataFrame
    df = pd.DataFrame(raw_data)
    
    # Sort by report date
    if 'period_of_report_date' in df.columns:
        df = df.sort_values('period_of_report_date', ascending=False)
    
    # Create exports directory if it doesn't exist
    os.makedirs('exports', exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'exports/{ticker}_raw_financial_data_{timestamp}.csv'
    
    # Export to CSV
    df.to_csv(filename, index=False)
    print(f"Raw financial data exported to {filename}")
    
    # Print column names to see available metrics
    print("\nAvailable metrics in the dataset:")
    for col in sorted(df.columns):
        print(f"- {col}")
    
    return filename


# Example usage in your main code:
async def analyze_and_export(ticker: str) -> None:
    """
    Fetch, analyze and export financial data for a single ticker.
    """
    try:
        service = PolygonFinancialService()
        async with service:
            # Fetch financial data
            financial_data = await service.fetch_financial_data(ticker)
            
            if financial_data:
                # Export to CSV
                csv_path = export_financial_data_to_csv(financial_data, ticker)
                print(f"Successfully exported {ticker} financial data to {csv_path}")
            else:
                print(f"No financial data available for {ticker}")
                
    except Exception as e:
        print(f"Error processing {ticker}: {str(e)}")

# Modified main function to include export
async def main():
    try:
        # Example usage for a single stock
        await analyze_and_export("AAPL")
        
        # Or for multiple stocks
        tech_stocks = ["AAPL", "MSFT", "GOOGL", "NVDA", "META"]
        for ticker in tech_stocks:
            await analyze_and_export(ticker)
            
    except Exception as e:
        print(f"Main execution error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())