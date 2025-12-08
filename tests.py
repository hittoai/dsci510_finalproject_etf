# tests.py
# Simple tests to make sure my helper functions run on small dummy data.
# These are NOT meant to be rigorous finance tests.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.fetch import get_prices
from src.compounding import contribution_path, monthly_needed_to_target
from src.metrics import cagr, ann_vol, max_drawdown, sharpe


def _dummy_price_series():
    dates = [datetime.today() - timedelta(days=i) for i in range(252)][::-1]
    prices = np.linspace(100, 120, len(dates))
    return pd.Series(prices, index=dates)


def test_contribution_path_length():
    s = contribution_path(200, years=10)
    assert len(s) == 10 * 12 + 1


def test_monthly_needed_has_values():
    df = monthly_needed_to_target(range(25, 30))
    assert df["Monthly Needed ($)"].notna().all()


def test_metrics_do_not_crash():
    s = _dummy_price_series()
    assert not np.isnan(cagr(s))
    assert not np.isnan(ann_vol(s))
    assert not np.isnan(max_drawdown(s))
    assert not np.isnan(sharpe(s))


def test_get_prices_returns_dataframe():
    # small smoke test for data loading
    df = get_prices(["SPY"], start="2020-01-01", end="2020-01-10")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
