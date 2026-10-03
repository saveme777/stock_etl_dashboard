import re
import yfinance as yf
import pandas as pd


def extract_and_load(ticker: str) -> pd.DataFrame:
    ticker = ticker.strip().upper()
    if not re.fullmatch(r"[A-Z0-9.^=-]{1,20}", ticker):
        raise ValueError("Enter a valid ticker using letters, numbers, and symbols like '.', '^', '=', '-'.")

    table = yf.download(ticker, period="1mo", interval="1d")
    if table.empty:
        raise ValueError(f"No stock data was found for {ticker}.")

    if isinstance(table.columns, pd.MultiIndex):
        table.columns = table.columns.get_level_values(0)

    table = table.dropna()
    if table.empty:
        raise ValueError(f"No usable stock data was found for {ticker}.")

    table["SMA"] = table["Close"].rolling(window=5).mean()
    table["Daily_Return"] = table["Close"].pct_change() * 100

    return table


if __name__ == "__main__":
    user_input_ticker = input(
        "Input the stock name (e.g., AAPL, NVDA, TSLA): "
    ).strip().upper()
    ticker = user_input_ticker or "AAPL"
    print(extract_and_load(ticker).tail(10))
