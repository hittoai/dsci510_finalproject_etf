# src/compounding.py
# Math-only compounding functions and charts

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from src.config import DEFAULT_RETURN

# constant monthly contribution with constant return
def contribution_path(monthly, years, annual_return=DEFAULT_RETURN):
    # total months
    months = years * 12

    # monthly return rate
    r = annual_return / 12.0

    balance = 0.0
    values = []

    # grow balance month by month
    for _ in range(months + 1):
        values.append(balance)
        balance = balance * (1.0 + r) + monthly

    return pd.Series(values, index=range(months + 1))


# compute monthly contribution needed to hit a target
def monthly_needed_to_target(start_ages,
                             target=1_000_000,
                             end_age=65,
                             annual_return=DEFAULT_RETURN):

    r = annual_return / 12.0
    rows = []

    for age in start_ages:
        months = (end_age - age) * 12

        if months <= 0:
            monthly = np.nan
        else:
            if r == 0:
                monthly = target / months
            else:
                factor = ((1.0 + r) ** months - 1.0) / r
                monthly = target / factor

        rows.append((age, monthly))

    df = pd.DataFrame(rows, columns=["Start Age", "Monthly Needed ($)"])
    return df


# start early vs start late chart
def chart_start_early_vs_late(outpath,
                              end_age=65,
                              annual_return=DEFAULT_RETURN):

    start_ages = [22, 32, 42]
    monthly_levels = [200, 500, 1000]

    plt.figure(figsize=(10, 6))
    max_val = 0.0

    for monthly in monthly_levels:
        for age in start_ages:
            years = end_age - age
            series = contribution_path(monthly, years, annual_return)
            label = f"Start {age}, ${monthly}/mo"
            plt.plot(series.index, series.values, label=label)
            max_val = max(max_val, series.max())

    plt.title(f"Starting Early vs Late at Different Monthly Contributions "
              f"({annual_return * 100:.0f}% annual return)")
    plt.xlabel("Months of Investing")
    plt.ylabel("Portfolio Value ($ in millions)")

    # scale y-axis in millions
    max_millions = max_val / 1_000_000
    step = 0.5
    upper = step * np.ceil(max_millions / step)

    ax = plt.gca()
    ax.set_ylim(0, upper * 1_000_000)
    ticks = np.arange(0, upper * 1_000_000 + 1, step * 1_000_000)
    ax.set_yticks(ticks)
    ax.yaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, _: f"${x / 1_000_000:.1f}M")
    )

    plt.legend(fontsize=8)
    plt.grid(True, linestyle=":", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


# early small vs late big chart
def chart_early_small_vs_late_big(outpath,
                                  end_age=65,
                                  annual_return=DEFAULT_RETURN):

    scenarios = [
        (22, 200),
        (32, 400),
        (42, 600),
        (52, 800),
    ]

    plt.figure(figsize=(10, 6))
    max_val = 0.0

    for age, monthly in scenarios:
        years = end_age - age
        series = contribution_path(monthly, years, annual_return)
        label = f"Start {age}, ${monthly}/mo"
        plt.plot(series.index, series.values, label=label)
        max_val = max(max_val, series.max())

    plt.title(f"Trying to Catch Up: Start Later with More Money "
              f"({annual_return * 100:.0f}% annual return)")
    plt.xlabel("Months of Investing")
    plt.ylabel("Portfolio Value ($ in millions)")

    max_millions = max_val / 1_000_000
    step = 0.2
    upper = step * np.ceil(max_millions / step)

    ax = plt.gca()
    ax.set_ylim(0, upper * 1_000_000)
    ticks = np.arange(0, upper * 1_000_000 + 1, step * 1_000_000)
    ax.set_yticks(ticks)
    ax.yaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, _: f"${x / 1_000_000:.1f}M")
    )

    plt.legend()
    plt.grid(True, linestyle=":", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


# single return monthly to $1M chart
def chart_monthly_to_1M(outpath,
                        target=1_000_000,
                        end_age=65,
                        annual_return=DEFAULT_RETURN):

    start_ages = range(18, 56)
    df = monthly_needed_to_target(start_ages, target, end_age, annual_return)

    plt.figure(figsize=(10, 6))
    plt.plot(df["Start Age"], df["Monthly Needed ($)"])
    plt.title(f"Monthly Savings Needed to Reach ${target:,.0f} by Age {end_age} "
              f"({annual_return * 100:.0f}% annual return)")
    plt.xlabel("Start Age")
    plt.ylabel("Monthly Needed ($)")
    plt.grid(True, linestyle=":", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


# multiple return monthly to $1M chart
def chart_monthly_to_1M_multi_returns(
        outpath,
        target=1_000_000,
        end_age=65,
        returns=(DEFAULT_RETURN,)
):

    start_ages = range(18, 56)

    plt.figure(figsize=(10, 6))
    plt.title(f"Monthly Savings to Reach ${target:,.0f} by Age {end_age}\n"
              f"Different Annual Return Assumptions")
    plt.xlabel("Start Age")
    plt.ylabel("Monthly Needed ($)")
    plt.grid(True, linestyle=":", linewidth=0.5)

    for r in returns:
        df = monthly_needed_to_target(start_ages, target, end_age, r)
        label = f"{int(r * 100)}% return"
        plt.plot(df["Start Age"], df["Monthly Needed ($)"], label=label)

    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

# DCA using ETF CAGR
def dca_constant_return(cagr_value,
                        monthly=200.0,
                        start_age=22,
                        end_age=65):

    years = end_age - start_age
    return contribution_path(monthly, years, annual_return=cagr_value)
