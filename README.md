# StrategiesBacktest

A Python-based backtesting framework for evaluating multiple options trading strategies using historical market data from Yahoo Finance. The project simulates strategy execution, calculates performance metrics, and visualizes cumulative profit and loss (PnL) over time.

## Features

* Historical stock price retrieval using Yahoo Finance (`yfinance`)
* Backtesting support for multiple trading strategies:

  * Straddle
  * Strangle
  * Iron Condor
  * Butterfly Spread
* Transaction cost and slippage modeling
* Performance analytics:

  * Annualized Return
  * Sharpe Ratio
  * Maximum Drawdown
  * Win/Loss Ratio
* Automated cumulative PnL visualization using Matplotlib
* Configurable ticker symbols and date ranges

## Tech Stack

* Python
* Pandas
* NumPy
* Matplotlib
* yFinance

## Strategy Logic

The framework evaluates market conditions using daily price movements and generates entry/exit signals based on predefined percentage thresholds.

Each strategy:

* Monitors daily price changes
* Opens positions when volatility exceeds a specified threshold
* Closes positions when volatility contracts
* Accounts for transaction costs and slippage during execution

## Performance Metrics

For each strategy, the framework computes:

* Annualized Return
* Sharpe Ratio
* Maximum Drawdown
* Win/Loss Ratio
* Cumulative Profit & Loss (PnL)

## Installation

```bash
pip install yfinance pandas numpy matplotlib
```

## Usage

```bash
python strategies_backtest.py
```

Modify the following parameters to test different assets and time periods:

```python
ticker = "MSFT"
start_date = "2019-01-01"
end_date = "2024-12-31"
```

## Sample Strategies Tested

* Straddle Strategy
* Strangle Strategy
* Iron Condor Strategy
* Butterfly Spread Strategy

## Project Structure

```text
StrategiesBacktest/
│
├── strategies_backtest.py
└── README.md
```

## Learning Objectives

This project demonstrates:

* Quantitative Finance Concepts
* Trading Strategy Backtesting
* Performance Evaluation Metrics
* Market Data Analysis
* Object-Oriented Programming in Python
* Financial Data Visualization
