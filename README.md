# DSCI 510 Final Project – Building a Set-and-Forget ETF Strategy for Graduate Students

This project is my final project for DSCI 510: Principles of Programming for Data Science (Fall 2025, USC).

The goal is to use simple Python code and real ETF price data to show how graduate students can build a long-term “set and forget” investing plan. I focus on dollar-cost averaging (DCA) into ETFs and how starting early, choice of ETF, and contribution size change the final outcome.

This project is for learning only. It is not financial advice.

---

## Introduction

Many students do not think about investing until much later in life.  
In this project I use historical ETF data and simple compounding math to answer a few questions:

1. How have a few popular ETFs performed in terms of return and risk?
2. How much per month is needed to reach \$1,000,000 by age 65 at different starting ages?
3. What is the impact of starting early versus starting later with larger contributions?
4. What happens if a student picks different ETFs while investing the same \$200/month?

All analysis is done in Python with short functions and simple loops.

---

## Data sources

Below is the data I used in the project.  
I do not upload any raw data files to this repository. All data is fetched by code when you run the project.

| Source                         | Type            | What it contains                                                    | How it is used                                  | Data scale (final)                          |
|--------------------------------|-----------------|---------------------------------------------------------------------|-------------------------------------------------|---------------------------------------------|
| Yahoo Finance via `yfinance`   | Historical ETF prices | Daily adjusted close prices for QQQ, SCHD, SPY, VIG, VTI, VUG from 2010-01-01 to present | Used to compute CAGR, volatility, Sharpe, and max drawdown for each ETF | ~3,800 trading days per ETF × 6 ETFs ≈ 22,800 price records |
| Derived monthly returns (code) | Computed metrics | Monthly returns, cumulative index series (rebased to 100)          | Plots for ETF growth and risk/return scatter    | Created in memory from Yahoo price data     |
| Simple compounding simulations | Computed sequences | Synthetic “what if” paths (start early vs late, catch-up scenarios, \$1M by 65) | Show the impact of start age and deposit size   | Series up to 43 years of monthly values     |

No API keys are needed for this project.

---

## Analysis

The analysis has two parts:

1. **ETF performance analysis**
   - Download daily adjusted close prices for QQQ, SCHD, SPY, VIG, VTI, VUG.
   - Compute:
     - CAGR (compound annual growth rate)
     - Annualized volatility
     - Max drawdown
     - Simple Sharpe ratio with 0% risk-free rate
   - Create:
     - An ETF growth chart (rebased so each ETF starts at 100)
     - A risk vs return scatter plot

2. **Compounding simulations for students**
   - Simple math-only simulations with a fixed annual return and monthly deposits:
     - Monthly savings needed to reach \$1,000,000 by age 65 for different start ages.
     - The effect of starting at 22 vs 32 vs 42 at different contribution levels.
     - “Trying to catch up” scenarios where late starters save more per month.
     - \$200/month DCA into a single ETF (QQQ, SPY, VIG) from age 22 to 65 using assumed returns.

All code is in plain Python with no machine learning models.  
The goal is to understand long-term compounding and risk/return trade-offs, not to forecast the market.

---

## Summary of results

Some key takeaways from the analysis:

- Growth-oriented ETFs like QQQ had the highest historical CAGR but also higher volatility and larger drawdowns.
- Dividend and “quality” ETFs like SCHD and VIG showed steadier returns with lower volatility.
- Starting earlier matters a lot more than trying to “catch up” later with bigger monthly deposits.  
  For example, someone who starts in their early 20s with a modest amount per month can often beat someone who starts in their 40s with much larger contributions.
- The monthly amount required to reach \$1,000,000 by age 65 grows very quickly as the starting age increases.
- Even when investing the same \$200/month, the final portfolio value can be very different depending on which ETF is chosen.

The slides in `docs/Sangwoo_Choi_presentation.pdf` give a visual summary of these results.

---

## Project structure

```text
.
├── docs/
│   ├── Sangwoo_Choi_progress_report.pdf
│   └── Sangwoo_Choi_presentation.pdf
├── src/
│   ├── config.py
│   ├── compounding.py
│   ├── fetch.py
│   ├── metrics.py
│   └── viz.py
├── main.py
├── tests.py
├── requirements.txt
├── README.md
└── .gitignore


## How to run

1. Make sure you have Python 3.10 or newer.

2. Download this project or clone the repository, then open a terminal in the project folder.

3. (Optional) Create a virtual environment.

On macOS or Linux:

    python -m venv venv
    source venv/bin/activate

On Windows:

    python -m venv venv
    venv\Scripts\activate

4. Install the required packages:

    pip install -r requirements.txt

5. Run the main script:

    python main.py

This will download the ETF data, calculate the metrics, and save all charts and CSV files into the `results` folder.

6. (Optional) If you want to view the results in a notebook, open `results.ipynb` and run the cells from top to bottom.

