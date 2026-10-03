import yfinance as yf
import pandas as pd 

ticker = "AAPL"

table = yf.download(ticker, period='1mo', interval='1d')
table = table.dropna()

table['SMA'] = table['Close'].rolling(window=5).mean() 
file_name = f"{ticker}_table.csv"

table['Daily_Return'] = table['Close'].pct_change() * 100
file_name = f"{ticker}_transformed.csv"
table.to_csv(file_name)

print(table.tail(10))

