# src/metrics.py
# Basic ETF metrics:
# CAGR, volatility, drawdown, Sharpe ratio

import numpy as np
import pandas as pd


# compute daily percent returns
def _daily_returns(price_series):
    return price_series.pct_change().dropna()


# compute CAGR
def cagr(price_series):
    price_series = price_series.dropna()
    if len(price_series) < 2:
        return np.nan

    start_price = price_series.iloc[0]
    end_price = price_series.iloc[-1]

    days = (price_series.index[-1] - price_series.index[0]).days
    years = days / 365.25

    if start_price <= 0 or years <= 0:
        return np.nan

    growth = end_price / start_price
    return growth ** (1.0 / years) - 1.0


# compute annualized volatility
def ann_vol(price_series):
    rets = _daily_returns(price_series)
    if len(rets) == 0:
        return np.nan

    daily_std = rets.std()
    return daily_std * np.sqrt(252)


# compute max drawdown
def max_drawdown(price_series):
    price_series = price_series.dropna()
    if len(price_series) == 0:
        return np.nan

    running_max = price_series.cummax()
    drawdowns = (price_series - running_max) / running_max
    return drawdowns.min()


# compute Sharpe ratio
def sharpe(price_series, rf_annual=0.0):
    r = cagr(price_series)
    v = ann_vol(price_series)

    if v == 0 or np.isnan(v):
        return np.nan

    return (r - rf_annual) / v
