# backtest.py

import pandas as pd
from stats_calculator import calculate_turnover  # Import the turnover function

class Backtest:
    def __init__(self, strategies, benchmark):
        self.strategies = strategies  # List of strategy instances
        self.benchmark = benchmark
        self.returns_dict = {}

    def run_backtest(self):
        # Ensure benchmark returns are included
        self.returns_dict['Benchmark'] = {
            'returns': self.benchmark.returns,
            'turnover': self.benchmark.turnover,
            'trading_frequency': self.benchmark.trading_frequency
        }

        # Run each strategy
        for strategy in self.strategies:
            strategy_name = strategy.name  # Each strategy should have a unique name
            strategy.generate_signals()
            signals = strategy.get_signals()
            # Calculate strategy returns
            returns_data = self.calculate_strategy_returns(strategy, signals)
            # Merge returns_dict with returns_data
            self.returns_dict.update(returns_data)

    def calculate_strategy_returns(self, strategy, signals):
        asset_returns = signals['asset_returns']
        trading_frequency = signals['trading_frequency']
        config = strategy.config

        returns_data = {}

        if strategy.legs == 'ALL':
            positions_dict = signals['positions']  # This is a dict with 'Long', 'Short', 'Combined'

            for leg_name, positions in positions_dict.items():
                # Calculate turnover using the imported function
                turnover = calculate_turnover(positions)
                # Calculate strategy returns
                strategy_returns = (asset_returns * positions).sum(axis=1)
                # Adjust returns for transaction costs
                adjusted_returns = self.adjust_returns_for_transaction_costs(strategy_returns, turnover, config)
                key = f"{strategy.name} - {leg_name}"
                returns_data[key] = {
                    'returns': adjusted_returns,
                    'turnover': turnover,
                    'trading_frequency': trading_frequency
                }
        else:
            positions = signals['positions']
            # Calculate turnover using the imported function
            turnover = calculate_turnover(positions)
            # Calculate strategy returns
            strategy_returns = (asset_returns * positions).sum(axis=1)
            # Adjust returns for transaction costs
            adjusted_returns = self.adjust_returns_for_transaction_costs(strategy_returns, turnover, config)
            leg_name = {'L': 'Long', 'S': 'Short', 'LS': 'Combined'}[strategy.legs]
            key = f"{strategy.name} - {leg_name}"
            returns_data[key] = {
                'returns': adjusted_returns,
                'turnover': turnover,
                'trading_frequency': trading_frequency
            }

        return returns_data

    def adjust_returns_for_transaction_costs(self, returns, turnover, config):
        """
        Adjust returns based on transaction costs derived from turnover.
        
        Parameters:
            returns (pd.Series): Series of strategy returns.
            turnover (pd.Series): Series of turnover values.
            config (Config): Configuration object containing transaction cost settings.
        
        Returns:
            pd.Series: Adjusted returns after accounting for transaction costs.
        """
        transaction_costs = turnover * (config.transaction_cost_bps / 10000)
        adjusted_returns = returns - transaction_costs
        return adjusted_returns

    def get_returns(self):
        return self.returns_dict
