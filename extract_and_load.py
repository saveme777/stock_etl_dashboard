import re
import yfinance as yf
import pandas as pd

def _normalize_ticker(ticker: str) -> str:
    return ticker.strip().upper()

def extract_and_load(ticker: str) -> tuple[pd.DataFrame, str]:
    ticker = _normalize_ticker(ticker)

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

    stock = yf.Ticker(ticker)

    info = stock.info
    company_name = info.get('longName') or info.get('shortName') or ticker

    return table, company_name


if __name__ == "__main__":
    user_input_ticker = input(
        "Input the stock name (e.g., AAPL, NVDA, TSLA): "
    ).strip().upper()
    ticker = user_input_ticker or "AAPL"
    data, company_name = extract_and_load(ticker)
    print(company_name)
    print(data.tail(10))
