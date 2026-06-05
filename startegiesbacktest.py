#!pip install yfinance

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load or generate model data from yfinance
def fetch_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data['Close']

# Fetching data for a specific stock (e.g., MSFT) over a specified period
ticker = 'MSFT'
start_date = '2019-01-01'
end_date = '2024-12-31'
prices = fetch_data(ticker, start_date, end_date)

# Define Strategy Classes
class Strategy:
    def __init__(self, data, transaction_cost=0.001, slippage=0.001):
        self.data = data
        self.transaction_cost = transaction_cost
        self.slippage = slippage
        self.positions = []
        self.pnl = []

    def execute(self):
      for i in range(1, len(self.data)):
          price_today = self.data.iloc[i]
          price_yesterday = self.data.iloc[i-1]
          if self.is_signal(price_today, price_yesterday):
              self.enter_position(price_today)
          elif self.is_exit(price_today, price_yesterday):
              self.exit_position(price_today)
          self.pnl.append(self.calculate_daily_pnl(price_today))


    def is_signal(self, price_today, price_yesterday):
        raise NotImplementedError

    def is_exit(self, price_today, price_yesterday):
        raise NotImplementedError

    def enter_position(self, price):
        raise NotImplementedError

    def exit_position(self, price):
        raise NotImplementedError

    def calculate_daily_pnl(self, price):
        return sum(self.positions) if self.positions else 0.0

class StraddleStrategy(Strategy):
    def is_signal(self, price_today, price_yesterday):
        return abs(price_today - price_yesterday) / price_yesterday > 0.01

    def is_exit(self, price_today, price_yesterday):
        return abs(price_today - price_yesterday) / price_yesterday < 0.005

    def enter_position(self, price):
        entry_cost = price * (1 + self.transaction_cost + self.slippage)
        self.positions.append(-entry_cost)

    def exit_position(self, price):
        exit_cost = price * (1 - self.transaction_cost - self.slippage)
        self.positions.append(exit_cost)

class StrangleStrategy(Strategy):
    def is_signal(self, price_today, price_yesterday):
        return abs(price_today - price_yesterday) / price_yesterday > 0.015

    def is_exit(self, price_today, price_yesterday):
        return abs(price_today - price_yesterday) / price_yesterday < 0.007

    def enter_position(self, price):
        entry_cost = price * (1 + self.transaction_cost + self.slippage)
        self.positions.append(-entry_cost)

    def exit_position(self, price):
        exit_cost = price * (1 - self.transaction_cost - self.slippage)
        self.positions.append(exit_cost)

class IronCondorStrategy(Strategy):
    def is_signal(self, price_today, price_yesterday):
        return abs(price_today - price_yesterday) / price_yesterday > 0.02

    def is_exit(self, price_today, price_yesterday):
        return abs(price_today - price_yesterday) / price_yesterday < 0.01

    def enter_position(self, price):
        entry_cost = price * (1 + self.transaction_cost + self.slippage)
        self.positions.append(-entry_cost)

    def exit_position(self, price):
        exit_cost = price * (1 - self.transaction_cost - self.slippage)
        self.positions.append(exit_cost)

class ButterflySpreadStrategy(Strategy):
    def is_signal(self, price_today, price_yesterday):
        return abs(price_today - price_yesterday) / price_yesterday > 0.025

    def is_exit(self, price_today, price_yesterday):
        return abs(price_today - price_yesterday) / price_yesterday < 0.012

    def enter_position(self, price):
        entry_cost = price * (1 + self.transaction_cost + self.slippage)
        self.positions.append(-entry_cost)

    def exit_position(self, price):
        exit_cost = price * (1 - self.transaction_cost - self.slippage)
        self.positions.append(exit_cost)

# Implement Backtesting and Performance Metrics Calculation
def backtest_strategy(strategy_class, data):
    data = data.squeeze()  # ensures Series, not DataFrame
    strategy = strategy_class(data)
    strategy.execute()

    pnl_series = pd.Series(strategy.pnl, index=data.index[1:])
    total_pnl = pnl_series.sum()
    total_return = total_pnl / len(data)
    num_years = (data.index[-1] - data.index[0]).days / 365.25

    if total_return <= -1:
        annualized_return = -1
    else:
        annualized_return = (1 + total_return) ** (1 / num_years) - 1

    sharpe_ratio = pnl_series.mean() / pnl_series.std() * np.sqrt(252) if pnl_series.std() != 0 else 0
    max_drawdown = (pnl_series.cumsum().expanding().max() - pnl_series.cumsum()).max() if len(pnl_series) > 0 else 0
    win_count = pnl_series[pnl_series > 0].count()
    loss_count = pnl_series[pnl_series <= 0].count()
    win_loss_ratio = win_count / loss_count if loss_count != 0 else float('inf')

    return {
        'annualized_return': annualized_return,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'win_loss_ratio': win_loss_ratio,
        'pnl_series': pnl_series
    }

# Backtest All Strategies
strategies = {
    'Straddle': StraddleStrategy,
    'Strangle': StrangleStrategy,
    'Iron Condor': IronCondorStrategy,
    'Butterfly Spread': ButterflySpreadStrategy
}

results = {name: backtest_strategy(strategy, prices) for name, strategy in strategies.items()}

# Reporting
for name, result in results.items():
    print(f"--- {name} Strategy ---")
    print(f"Annualized Return: {result['annualized_return']:.2%}")
    print(f"Sharpe Ratio: {result['sharpe_ratio']:.2f}")
    print(f"Maximum Drawdown: {result['max_drawdown']:.2f}")
    print(f"Win/Loss Ratio: {result['win_loss_ratio']:.2f}") if result['win_loss_ratio'] != float('inf') else print("Win/Loss Ratio: All Wins")
    plt.figure(figsize=(10, 6))
    plt.plot(result['pnl_series'].cumsum(), label=f'{name} Cumulative PnL')
    plt.title(f'{name} Strategy Performance')
    plt.xlabel('Date')
    plt.ylabel('Cumulative PnL')
    plt.legend()
    plt.grid(True)
    plt.show()
