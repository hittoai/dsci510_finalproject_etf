# src/fetch.py
# download ETF prices from Yahoo Finance

import pandas as pd
import yfinance as yf

def get_prices(tickers, start="2010-01-01", end=None):
    # make sure tickers is a list
    if isinstance(tickers, str):
        tickers = [tickers]

    data = yf.download(
        tickers,
        start=start,
        end=end,
        progress=False,
        auto_adjust=True,
        threads=False,
    )

    # keep only the Close prices
    if isinstance(data.columns, pd.MultiIndex):
        close = data["Close"]
    else:
        close = data[["Close"]]
        close.columns = tickers

    close = close.dropna(how="all")
    return close
