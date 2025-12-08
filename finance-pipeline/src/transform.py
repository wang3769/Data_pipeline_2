import pandas as pd

def compute_returns(df):
    """
    Compute daily returns from historical stock prices.

    Parameters:
    df (pandas.DataFrame): A DataFrame containing historical stock prices with a 'Close' column.

    Returns:
    pandas.DataFrame: A DataFrame with an additional 'Returns' column representing daily returns.
    """
    df['Returns'] = df['Close'].pct_change()
    return df

def compute_features(df):
    """
    Compute additional financial features from historical stock prices.

    Parameters:
    df (pandas.DataFrame): A DataFrame containing historical stock prices with a 'Close' column.

    Returns:
    pandas.DataFrame: A DataFrame with additional columns for moving averages.
    """
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['Vol20'] = df['Close'].rolling(window=50).std()
    return df