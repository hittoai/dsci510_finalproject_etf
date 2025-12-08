# tests.py
# simple tests to check that core functions run

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.compounding import contribution_path, monthly_needed_to_target
from src.metrics import cagr, ann_vol, max_drawdown, sharpe


# make a fake price series that slowly goes up
def _dummy_price_series():
    dates = [datetime.today() - timedelta(days=i) for i in range(252)][::-1]
    prices = np.linspace(100, 120, len(dates))
    return pd.Series(prices, index=dates)


# test length of contribution_path output
def test_contribution_path_length():
    s = contribution_path(200, years=10)
    assert len(s) == 10 * 12 + 1


# test that monthly_needed_to_target returns non-empty numbers
def test_monthly_needed_has_values():
    df = monthly_needed_to_target(range(25, 30))
    assert df["Monthly Needed ($)"].notna().all()


# test that metric functions return numbers (not NaN)
def test_metrics_do_not_crash():
    s = _dummy_price_series()
    assert not np.isnan(cagr(s))
    assert not np.isnan(ann_vol(s))
    assert not np.isnan(max_drawdown(s))
    assert not np.isnan(sharpe(s))
