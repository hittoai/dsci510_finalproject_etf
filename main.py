# main.py
# DSCI 510 Final Project
# Building a Set-and-Forget ETF Strategy for Graduate Students


from src.config import (
    RESULTS_DIR,
    TICKERS,
    START_DATE,
    DCA_MONTHLY,
    DCA_START_AGE,
    DCA_END_AGE,
    DCA_RETURNS,
)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from src.fetch import get_prices
from src.metrics import cagr, ann_vol, max_drawdown, sharpe
from src.viz import line_chart, risk_return_scatter
from src.compounding import (
    chart_start_early_vs_late,
    chart_early_small_vs_late_big,
    chart_monthly_to_1M,
    chart_monthly_to_1M_multi_returns,
    dca_constant_return,
)


# run all compounding charts
def run_compounding_visuals():
    print("Creating compounding charts...")

    chart_start_early_vs_late(RESULTS_DIR / "early_vs_late_200mo.png")
    chart_early_small_vs_late_big(RESULTS_DIR / "early_small_vs_late_big.png")
    chart_monthly_to_1M(RESULTS_DIR / "monthly_needed_to_1M.png")

    chart_monthly_to_1M_multi_returns(
        RESULTS_DIR / "monthly_to_1M_multi_returns.png",
        returns=(0.07, 0.09, 0.13, 0.15, 0.20),
    )


# run ETF data download, metrics, and charts
def run_etf_analysis():
    print("Fetching ETF prices and metrics...")

    # get daily adjusted close prices
    prices = get_prices(TICKERS, start=START_DATE, end=None)
    prices.to_csv(RESULTS_DIR / "prices.csv")

    # compute metrics for each ETF
    rows = []
    for ticker in prices.columns:
        s = prices[ticker].dropna()
        row = {
            "Ticker": ticker,
            "CAGR": round(cagr(s), 4),
            "AnnualVolatility": round(ann_vol(s), 4),
            "MaxDD": round(max_drawdown(s), 4),
            "Sharpe(0%)": round(sharpe(s, rf_annual=0.0), 4),
        }
        rows.append(row)

    metrics_df = pd.DataFrame(rows)
    metrics_df.to_csv(RESULTS_DIR / "metrics.csv", index=False)

    # rebase ETFs so each starts at 100
    rebased = prices.copy()

    for col in rebased.columns:
        first_valid = rebased[col].dropna()
        if len(first_valid) == 0:
            continue
        first_price = first_valid.iloc[0]
        rebased[col] = rebased[col] / first_price * 100.0

    line_chart(
        rebased,
        title="ETF Growth (rebased to 100)",
        xlab="Date",
        ylab="Index (Start = 100)",
        out_path=RESULTS_DIR / "etf_growth.png",
    )

    # risk vs return scatter chart
    risk_return_scatter(metrics_df, RESULTS_DIR / "risk_return_scatter.png")

    # $200/month DCA from age 22 to 65
    print("Simulating $200/month DCA into single ETFs (22 to 65)...")

    dca_tickers = list(DCA_RETURNS.keys())
    dca_df = pd.DataFrame()

    for t in dca_tickers:
        r = DCA_RETURNS[t]
        series = dca_constant_return(
            cagr_value=r,
            monthly=DCA_MONTHLY,
            start_age=DCA_START_AGE,
            end_age=DCA_END_AGE,
        )
        dca_df[t] = series.values

    # plot DCA results
    plt.figure(figsize=(10, 6))

    for col in dca_df.columns:
        plt.plot(range(len(dca_df)), dca_df[col], label=col)

    ax = plt.gca()

    # x-axis: ages from config
    start_age = DCA_START_AGE
    end_age = DCA_END_AGE
    ages = list(range(start_age, end_age + 1, 5))
    age_months = [(age - start_age) * 12 for age in ages]
    ax.set_xticks(age_months)
    ax.set_xticklabels([str(age) for age in ages])

    # y-axis: 1 million dollar steps
    max_val = dca_df.max().max()
    step_dollars = 1_000_000
    upper = step_dollars * np.ceil(max_val / step_dollars)

    ax.set_ylim(0, upper)
    ticks = np.arange(0, upper + step_dollars, step_dollars)
    ax.set_yticks(ticks)
    ax.yaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, _: f"${x / 1_000_000:.0f}M")
    )

    plt.title(
        "Investing $200/Month in a Single ETF (DCA)\n"
        "Modeled from Age 22 to 65 using ETF Historical CAGR"
    )
    plt.xlabel("Age")
    plt.ylabel("Portfolio Value ($ in millions)")
    plt.legend()
    plt.grid(True, linestyle=":", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "dca_200_single_etf.png")
    plt.close()


if __name__ == "__main__":
    print("Generating compounding visuals...")
    run_compounding_visuals()
    run_etf_analysis()
    print("Done. See PNG and CSV files in /results")
