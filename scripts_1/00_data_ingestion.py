import requests

# Replace this with your actual API key
API_KEY = '1e5d2c3ffeb645cf86d1200c110c0a6f'
#wangtianqi2012@hotmail
#1234567AB

# Define the endpoint and parameters
url = 'https://newsapi.org/v2/top-headlines'
params = {
    'country': 'us',
    'category': 'business',  # options: business, entertainment, general, health, science, sports, technology
    'pageSize': 100,  # number of articles
    'apiKey': API_KEY
}

# Make the request
response = requests.get(url, params=params)

# Check if request was successful
if response.status_code == 200:
    data = response.json() # JSON is a standard for APIs, light and language agnostic
    articles = data.get('articles', []) # get returns default values of a dictionary in this case it specify a []

    # Print article details
    # for i, article in enumerate(articles, 1):
    #     print(f"\nArticle {i}")
    #     print(f"Title: {article['title']}")
    #     print(f"Description: {article['description']}")
    #     print(f"URL: {article['url']}")
    #     print(f"date: {article['publishedAt']}")
else:
    print("Error:", response.status_code, response.text)
    
import os
import sqlite3
import pandas as pd

folder_path = '../data/raw/'
#folder_path = "/opt/airflow/data/"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

os.chdir(folder_path)

#print("Current directory:", os.getcwd())

# Sample: convert articles list to a dataframe first
df = pd.DataFrame(articles)

# Flatten 'source' column (which is a dict)
df['source'] = df['source'].apply(lambda s: s['name'] if isinstance(s, dict) else s)

# Connect to SQLite file (creates if not exist)
conn = sqlite3.connect('news_data.db')

# Save to table called "articles"
df.to_sql('articles', conn, if_exists='append', index=False)

conn.close()

import yfinance as yf
from fredapi import Fred
from datetime import datetime, timedelta

# --- Configuration ---
# FRED API Key: Get this from https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY = "ed24853a8f0f94789ced07aded2551ef"  # <<< IMPORTANT: Replace with your actual FRED API key

# Define the SQLite database file name
DB_NAME = 'market_data.db'

# Define a reasonable start date for historical data
# For long-term analysis, you might go back further (e.g., '2000-01-01')
# For daily updates, focusing on recent data (e.g., last 5 years) is sufficient.
START_DATE = (datetime.now() - timedelta(days=5 * 365)).strftime('%Y-%m-%d')  # Last 5 years
END_DATE = datetime.now().strftime('%Y-%m-%d')  # Today

# --- Helper Function to Save to SQLite ---
def save_to_sqlite(df: pd.DataFrame, table_name: str, conn: sqlite3.Connection):
    """
    Saves a DataFrame to an SQLite table.
    Uses 'append' mode so new data is added, and 'replace' if the table structure needs to be reset.
    """
    if df.empty:
        print(f"Skipping empty DataFrame for table: {table_name}")
        return

    # To handle potential schema changes or initial creation,
    # we'll try to append. If an error occurs (e.g., table doesn't exist initially
    # or column mismatch), we'll replace. This is a robust strategy for a pipeline.
    try:
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Successfully appended data to table: '{table_name}'")
    except Exception as e:
        print(f"Error appending to '{table_name}' (possibly table not found or schema mismatch): {e}")
        print(f"Attempting to replace table: '{table_name}'")
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Successfully replaced data in table: '{table_name}'")

# --- Database Connection ---
conn = sqlite3.connect(DB_NAME)
print(f"Connected to SQLite database: {DB_NAME}")

# --- 1. S&P 500 and Magnificent 7 Stock Prices ---
print("\n--- Collecting Stock Prices ---")
SP500_TICKER = '^GSPC'  # S&P 500 Index
MAG7_TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']

all_stock_data_list = [] # Using a list to concatenate at the end for efficiency

# Fetch S&P 500 data
try:
    print(f"Fetching data for {SP500_TICKER} (S&P 500)...")
    sp500_data = yf.download(SP500_TICKER, start=START_DATE, end=END_DATE)
    if not sp500_data.empty:
        sp500_data['Ticker'] = SP500_TICKER
        sp500_data.reset_index(inplace=True) # Convert 'Date' index to a column
        all_stock_data_list.append(sp500_data)
        print(f"Successfully fetched {SP500_TICKER} data.")
    else:
        print(f"No data fetched for {SP500_TICKER}.")
except Exception as e:
    print(f"Error fetching {SP500_TICKER} data: {e}")

# Fetch Mag7 data
for ticker in MAG7_TICKERS:
    try:
        print(f"Fetching data for {ticker}...")
        stock_data = yf.download(ticker, start=START_DATE, end=END_DATE)
        if not stock_data.empty:
            stock_data['Ticker'] = ticker
            stock_data.reset_index(inplace=True) # Convert 'Date' index to a column
            all_stock_data_list.append(stock_data)
            print(f"Successfully fetched {ticker} data.")
        else:
            print(f"No data fetched for {ticker}.")
    except Exception as e:
        print(f"Error fetching {ticker} data: {e}")

if all_stock_data_list:
    final_stock_df = pd.concat(all_stock_data_list, ignore_index=True)
    # Ensure 'Date' column is in datetime format before saving to SQLite
    final_stock_df['Date'] = pd.to_datetime(final_stock_df['Date']).dt.date # Store as date object in SQLite
    save_to_sqlite(final_stock_df, 'stock_prices', conn)
else:
    print("No stock data collected to save.")


# --- 2. Treasury Yields (2yr, 10yr, 30yr) ---
print("\n--- Collecting Treasury Yields ---")
fred = Fred(api_key=FRED_API_KEY)

TREASURY_SERIES_IDS = {
    '2YR_TREASURY': 'DGS2',
    '10YR_TREASURY': 'DGS10',
    '30YR_TREASURY': 'DGS30'
}

all_treasury_data = pd.DataFrame()

for name, series_id in TREASURY_SERIES_IDS.items():
    try:
        print(f"Fetching data for {name} ({series_id})...")
        treasury_data = fred.get_series(series_id, observation_start=START_DATE, observation_end=END_DATE)
        if treasury_data is not None and not treasury_data.empty:
            treasury_data = pd.DataFrame(treasury_data).rename(columns={0: name})
            if all_treasury_data.empty:
                all_treasury_data = treasury_data
            else:
                # Use outer join to ensure all dates are included, even if one series has missing dates
                all_treasury_data = all_treasury_data.join(treasury_data, how='outer')
            print(f"Successfully fetched {name} data.")
        else:
            print(f"No data fetched for {name} ({series_id}).")
    except Exception as e:
        print(f"Error fetching {name} data: {e}")

if not all_treasury_data.empty:
    all_treasury_data.reset_index(inplace=True)
    all_treasury_data.rename(columns={'index': 'Date'}, inplace=True)
    all_treasury_data['Date'] = pd.to_datetime(all_treasury_data['Date']).dt.date # Store as date object
    save_to_sqlite(all_treasury_data, 'treasury_yields', conn)
else:
    print("No treasury data collected to save.")


# --- 3. USD Exchange to Few Other Currencies ---
print("\n--- Collecting Currency Exchange Rates ---")
CURRENCY_PAIRS = {
    'EURUSD': 'EURUSD=X',
    'USDJPY': 'JPY=X',  # JPY=X means USD/JPY
    'GBPUSD': 'GBPUSD=X',
    'USDCAD': 'CAD=X'   # CAD=X means USD/CAD
}

all_currency_data = pd.DataFrame()

for name, ticker in CURRENCY_PAIRS.items():
    try:
        print(f"Fetching data for {name} ({ticker})...")
        currency_data = yf.download(ticker, start=START_DATE, end=END_DATE)
        if not currency_data.empty:
            currency_data = pd.DataFrame(currency_data['Close']).rename(columns={'Close': name})
            if all_currency_data.empty:
                all_currency_data = currency_data
            else:
                all_currency_data = all_currency_data.join(currency_data, how='outer')
            print(f"Successfully fetched {name} data.")
        else:
            print(f"No data fetched for {name} ({ticker}).")
    except Exception as e:
        print(f"Error fetching {name} data: {e}")

if not all_currency_data.empty:
    all_currency_data.reset_index(inplace=True)
    all_currency_data.rename(columns={'index': 'Date'}, inplace=True)
    all_currency_data['Date'] = pd.to_datetime(all_currency_data['Date']).dt.date # Store as date object
    save_to_sqlite(all_currency_data, 'currency_exchange_rates', conn)
else:
    print("No currency data collected to save.")

# --- Close Database Connection ---
conn.close()
print(f"\nData collection complete and saved to '{DB_NAME}'!")