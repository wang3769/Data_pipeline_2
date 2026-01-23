from extract import download_prices
from transform import compute_features, compute_returns
from load import save_to_db
from config import load_config
import os

def run_pipeline():
    cfg = load_config()

    tickers = cfg["tickers"]
    start_date = cfg["date_range"]["start"]
    end_date = cfg["date_range"]["end"]
    for ticker in tickers:
        print(f"=== Processing {ticker} ===")
        # Step 1: Extract
        prices = download_prices(ticker, start_date, end_date)
        
        # Step 2: Transform
        features = compute_features(prices)
        returns = compute_returns(prices)
        
        # Combine features and returns into a single dataset
        # Select only the computed columns to avoid MultiIndex overlap
        dataset = prices[['Date']].copy()
        dataset['MA_20'] = features['MA_20']
        dataset['Vol20'] = features['Vol20']
        dataset['Returns'] = returns['Returns']
        
        # Step 3: Load
        # `save_to_db` expects the second parameter to be named `table` (or passed positionally).
        # Use the `table` keyword so the call matches `load.save_to_db` signature.
        save_to_db(dataset, table=f"{ticker}_data")

        print(f"Pipeline completed for {ticker} from {start_date} to {end_date}")


if __name__ == "__main__":
    run_pipeline()