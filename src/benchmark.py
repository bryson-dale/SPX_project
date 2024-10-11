# benchmark.py

import pandas as pd

class Benchmark:
    def __init__(self, data_loader, config):
        self.data_loader = data_loader
        self.config = config
        self.returns = None
        self.turnover = None
        self.trading_frequency = None  # Add trading_frequency attribute

    def calculate_returns(self, trading_frequency='M', start_date='1980-01-01', end_date=None):
        # Set trading_frequency attribute
        self.trading_frequency = trading_frequency.upper()

        # Get data
        prices = self.data_loader.get_prices()
        presence_matrix = self.data_loader.get_presence_matrix()

        # Resample data
        freq = self.trading_frequency
        prices = prices.resample(freq).last()
        presence_matrix = presence_matrix.resample(freq).last()

        # Filter dates
        start_date = pd.to_datetime(start_date)
        if end_date:
            end_date = pd.to_datetime(end_date)
            date_mask = (prices.index >= start_date) & (prices.index <= end_date)
        else:
            date_mask = prices.index >= start_date
        prices = prices.loc[date_mask]
        presence_matrix = presence_matrix.loc[date_mask]

        # Calculate returns
        returns = prices.pct_change()

        # Align returns and presence_matrix
        returns, presence_shifted = returns.align(presence_matrix.shift(1), join='inner', axis=1)

        # Multiply returns by shifted presence_matrix
        returns = returns.multiply(presence_shifted)

        # Equal-weighted portfolio weights
        weights = presence_shifted.div(presence_shifted.sum(axis=1), axis=0)

        # Calculate turnover
        turnover = weights.diff().abs().sum(axis=1)
        # Set initial turnover
        turnover.iloc[0] = weights.iloc[0].abs().sum()

        # Equal-weighted benchmark returns
        portfolio_returns = (returns * weights).sum(axis=1)

        # Assign returns and turnover
        self.returns = portfolio_returns.fillna(0)
        self.turnover = turnover.fillna(0)

        # Adjust returns for transaction costs
        transaction_costs = self.turnover * (self.config.transaction_cost_bps / 10000)
        self.returns = self.returns - transaction_costs
