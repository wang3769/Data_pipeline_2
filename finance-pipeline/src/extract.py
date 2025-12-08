import yfinance as yf

def download_prices(ticker, start, end):
    """
    Download historical stock prices for a given ticker symbol.

    Parameters:
    ticker (str): The stock ticker symbol.
    start (str): The start date for the data in 'YYYY-MM-DD' format.
    end (str): The end date for the data in 'YYYY-MM-DD' format.

    Returns:
    pandas.DataFrame: A DataFrame containing the historical stock prices.
    """
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    df.reset_index(inplace=True)
    print(f"  ✓ Downloaded {len(df)} rows of data for {ticker}")
    return df

if __name__ == "__main__":
    # Test with a single ticker
    print("Testing extract.py...")
    df = download_prices("AAPL", "2024-01-01", "2025-01-01")
    print(f"Returned DataFrame shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"First row:\n{df.head(1)}")