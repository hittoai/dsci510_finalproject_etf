import pytest
import yfinance as yf

def test_yfinance_api_fetch():

    try:
        df = yf.download("SPY", start="2020-01-01", end="2020-02-01", progress=False, threads=False)
    except Exception as e:
        pytest.skip(f"Network issue during API call: {e}")
    assert not df.empty
