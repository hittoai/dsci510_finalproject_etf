import yfinance as yf

def demo_fetch():
    """Fetch sample ETF data (SPY) to show API functionality"""
    df = yf.download("SPY", start="2020-01-01", end="2020-03-01", progress=False, threads=False)
    print(df.head())
    print(f"Fetched {len(df)} records for SPY")

if __name__ == "__main__":
    demo_fetch()
