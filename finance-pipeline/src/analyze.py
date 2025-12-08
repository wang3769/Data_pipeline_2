import matplotlib.pyplot as plt

def plot_price(df, ticker):
    plt.plot(df["Date"], df["Close"], label=ticker)
    plt.title(f"{ticker} Closing Prices Over Time")
    plt.show()

def compute_sharpe(df):
    return df["Returns"].mean() / df["Returns"].std() * (252 ** 0.5)