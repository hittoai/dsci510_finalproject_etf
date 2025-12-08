# src/config.py
# shared settings and constants for the project

from pathlib import Path

# folder for output files
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

# ETFs used in the project
TICKERS = ["QQQ", "SCHD", "SPY", "VIG", "VTI", "VUG"]

# start date for price history
START_DATE = "2010-01-01"

# default annual return used in compounding examples
DEFAULT_RETURN = 0.09  # 9%

# target and end age for $1M examples
TARGET_AMOUNT = 1_000_000
END_AGE = 65

