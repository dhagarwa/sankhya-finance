import yfinance as yf
import pandas as pd

def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    table = pd.read_html(url)[0]  # Read the first table on the page
    tickers = table["Symbol"].tolist()
    return tickers

def get_top_10_companies(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            data.append({
                "Ticker": ticker,
                "Company Name": info.get("longName", "N/A"),
                "Market Cap": info.get("marketCap", 0),
            })
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            continue

    df = pd.DataFrame(data)
    df = df[df["Market Cap"] > 0]  # Remove invalid data
    df = df.sort_values(by="Market Cap", ascending=False).head(10)
    return df

def fetch_fundamentals(tickers):
    fundamentals_data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            fundamentals_data.append({
                "Ticker": ticker,
                "Company Name": info.get("longName", "N/A"),
                "Sector": info.get("sector", "N/A"),
                "Industry": info.get("industry", "N/A"),
                "Market Cap": info.get("marketCap", "N/A"),
                "PE Ratio": info.get("trailingPE", "N/A"),
                "Dividend Yield": info.get("dividendYield", "N/A"),
                "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
                "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
                "Current Price": info.get("currentPrice", "N/A"),
            })
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            continue
    return pd.DataFrame(fundamentals_data)

def fetch_all_fundamentals(tickers):
    fundamentals_data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            fundamentals_data.append({"Ticker": ticker, **info})
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            continue
    return pd.DataFrame(fundamentals_data)

def main():
    # Fetch S&P 500 tickers
    sp500_tickers = get_sp500_tickers()
    print(f"Retrieved {len(sp500_tickers)} S&P 500 tickers.")

    # Get the top 10 companies
    top_10_companies = get_top_10_companies(sp500_tickers)
    print("\nTop 10 Companies by Market Cap:")
    print(top_10_companies)

    # Get tickers of the top 10 companies
    top_10_tickers = top_10_companies["Ticker"].tolist()

    # Fetch fundamentals for these companies
    fundamentals = fetch_fundamentals(top_10_tickers)
    print("\nFundamental Data for Top 10 Companies:")
    print(fundamentals)

    # Fetch all fundamentals
    all_fundamentals = fetch_all_fundamentals(top_10_tickers)
    print("\nAll Available Fundamental Data:")
    print(all_fundamentals)
    
    # Save column names to text file
    with open('yfinance_fundamentals.txt', 'w') as f:
        f.write('\n'.join(all_fundamentals.columns.tolist()))
    
if __name__ == "__main__":
    main()

