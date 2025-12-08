# src/viz.py
# All plotting functions for the ETF project
# Uses only matplotlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# apply larger readable font sizes for slides
def _apply_readable_style(ax, title_size=30, label_size=24, tick_size=20, legend_size=20):

    ax.title.set_fontsize(title_size)
    ax.xaxis.label.set_size(label_size)
    ax.yaxis.label.set_size(label_size)
    ax.tick_params(axis="both", labelsize=tick_size)

    leg = ax.get_legend()
    if leg is not None:
        for text in leg.get_texts():
            text.set_fontsize(legend_size)



# draw a simple line chart
def line_chart(df: pd.DataFrame, title: str, xlab: str, ylab: str, out_path: str):

    fig, ax = plt.subplots(figsize=(10, 6))

    for col in df.columns:
        ax.plot(df.index, df[col], label=str(col))

    ax.set_title(title)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.legend(loc="upper left")

    _apply_readable_style(ax)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


# ETF growth chart rebased to 100
def etf_growth_chart(prices_df: pd.DataFrame, out_path: str):

    rebased = prices_df / prices_df.iloc[0] * 100.0

    fig, ax = plt.subplots(figsize=(10, 6))

    for col in rebased.columns:
        ax.plot(rebased.index, rebased[col], label=col)

    ax.set_title("ETF Growth (rebased to 100)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Index level (start = 100)")
    ax.legend(loc="upper left")

    _apply_readable_style(ax)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


# risk vs return scatter plot
def risk_return_scatter(metrics_df: pd.DataFrame, out_path: str):

    fig, ax = plt.subplots(figsize=(8, 6))

    for _, row in metrics_df.iterrows():
        x = row["AnnualVolatility"]
        y = row["CAGR"]
        ticker = row["Ticker"]

        ax.scatter(x, y, s=80)

        # ETF label
        ax.text(x + 0.0005, y, ticker, fontsize=13, va="center")

    ax.set_title("Risk / Return Profile of ETFs")
    ax.set_xlabel("Annual volatility")
    ax.set_ylabel("CAGR (annual return)")

    _apply_readable_style(ax)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


# DCA $200/month into one ETF
def dca_200_single_etf(dca_df: pd.DataFrame, out_path: str):

    fig, ax = plt.subplots(figsize=(10, 6))

    start_age = 22
    end_age = 65

    total_months = len(dca_df)
    ages = list(range(start_age, end_age + 1, 5))
    age_positions = []

    for age in ages:
        months_from_start = (age - start_age) * 12
        if months_from_start < total_months:
            age_positions.append(months_from_start)

    for col in dca_df.columns:
        ax.plot(dca_df.index, dca_df[col] / 1_000_000.0, label=str(col))

    ax.set_xticks(age_positions)
    ax.set_xticklabels([str(age) for age in ages])

    ax.set_title("Investing $200/Month in a Single ETF (DCA)\nModeled from Age 22 to 65")
    ax.set_xlabel("Age")
    ax.set_ylabel("Portfolio Value ($ in millions)")
    ax.legend(loc="upper left")

    _apply_readable_style(ax)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


# start early vs late chart
def early_vs_late_200mo(results_dict: dict, out_path: str):

    fig, ax = plt.subplots(figsize=(10, 6))

    for label, series in results_dict.items():
        ax.plot(series.index, series.values, label=label)

    ax.set_title("Start Early vs Start Late\n$200/month DCA")
    ax.set_xlabel("Age")
    ax.set_ylabel("Portfolio value ($)")
    ax.legend(loc="upper left")

    _apply_readable_style(ax)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


# early small vs late big chart
def early_small_vs_late_big(results_dict: dict, out_path: str):

    fig, ax = plt.subplots(figsize=(10, 6))

    for label, series in results_dict.items():
        ax.plot(series.index, series.values, label=label)

    ax.set_title("Early Small vs Late Big Contributions")
    ax.set_xlabel("Age")
    ax.set_ylabel("Portfolio value ($)")
    ax.legend(loc="upper left")

    _apply_readable_style(ax)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


# monthly needed to reach $1M
def monthly_needed_to_1M(monthly_needed: pd.Series, out_path: str):

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(monthly_needed.index, monthly_needed.values, marker="o")

    ax.set_title(
        "Monthly Savings Needed to Reach $1,000,000 by Age 65\n(9% Annual Return)",
        fontsize=28
    )
    ax.set_xlabel("Start Age", fontsize=22)
    ax.set_ylabel("Monthly Needed ($)", fontsize=22)

    ax.tick_params(axis="both", labelsize=18)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)

# monthly to $1M with multiple returns
def monthly_to_1M_multi_returns(results_dict: dict, out_path: str):

    fig, ax = plt.subplots(figsize=(10, 6))

    for label, series in results_dict.items():
        ax.plot(series.index, series.values, label=label)

    ax.set_title(
        "Monthly Savings to Reach $1,000,000 by Age 65\nDifferent Annual Return Assumptions",
        fontsize=28
    )
    ax.set_xlabel("Start Age", fontsize=22)
    ax.set_ylabel("Monthly Needed ($)", fontsize=22)

    ax.tick_params(axis="both", labelsize=18)

    ax.legend(loc="upper left", fontsize=18)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)

