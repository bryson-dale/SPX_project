# strategy/momentum_sector_LS.py

import pandas as pd
import numpy as np
from .strategy_base import Strategy  # Relative import from strategy_base

class MomentumSectorLongShortStrategy(Strategy):
    def __init__(self, data_loader, config):
        self.name = 'Momentum Sector Long-Short Strategy'  # Unique name for the strategy
        self.data_loader = data_loader
        self.config = config
        self.set_parameters()
        # Initialize other necessary attributes
        self.long_positions = None
        self.short_positions = None
        self.combined_positions = None
        self.asset_returns = None
        self.trading_frequency = None
        self.start_date = None
        self.end_date = None
        self.invert_long = False
        self.invert_short = False
        self.legs = 'ALL'  # Default value
        # New attributes for presence matrices
        self.top_presence_matrix = None
        self.bottom_presence_matrix = None
        self.combined_presence_matrix = None

    def set_parameters(self, **kwargs):
        self.num_sectors = kwargs.get('num_sectors', 5)
        self.trading_frequency = kwargs.get('trading_frequency', 'M').upper()
        self.start_date = pd.to_datetime(kwargs.get('start_date', '1980-01-01'))
        self.end_date = pd.to_datetime(kwargs.get('end_date')) if kwargs.get('end_date') else None
        self.invert_long = kwargs.get('invert_long', False)
        self.invert_short = kwargs.get('invert_short', False)
        self.legs = kwargs.get('legs', 'ALL').upper()  # Accept 'L', 'S', 'LS', 'ALL'

        # Validate legs parameter
        valid_legs = ['L', 'S', 'LS', 'ALL']
        if self.legs not in valid_legs:
            raise ValueError(f"Invalid legs parameter. Expected one of {valid_legs}, got '{self.legs}'.")

    def generate_signals(self):
        # Get data from DataLoader
        prices = self.data_loader.get_prices()
        presence_matrix = self.data_loader.get_presence_matrix()

        # Resample data based on trading frequency
        freq = self.trading_frequency  # Use the pandas frequency string directly

        # Resample and compute returns
        spx_returns = prices.resample(freq).last().pct_change()
        presence_matrix_resampled = presence_matrix.resample(freq).last()

        # Filter data by date range
        if self.end_date:
            date_mask = (spx_returns.index >= self.start_date) & (spx_returns.index <= self.end_date)
        else:
            date_mask = spx_returns.index >= self.start_date
        spx_returns = spx_returns.loc[date_mask]
        presence_matrix_resampled = presence_matrix_resampled.loc[date_mask]

        # Apply presence matrix to returns
        spx500_returns = spx_returns.multiply(presence_matrix_resampled.shift(1), axis=0)

        # Remove columns with all NaNs
        spx500_returns = spx500_returns.dropna(axis=1, how='all')

        # Store for later use
        self.spx500_returns = spx500_returns

        # Calculate sector average returns
        sector_avg_returns = spx500_returns.groupby(axis=1, level='sector').mean()

        # Calculate sector momentum
        window_size = self._determine_window_size()
        sector_return_momentum = sector_avg_returns.shift(1).rolling(window=window_size-1, min_periods=1).mean()

        # Create presence matrices for top and bottom sectors
        top_presence_matrix = pd.DataFrame(0, index=sector_return_momentum.index, columns=sector_return_momentum.columns)
        bottom_presence_matrix = pd.DataFrame(0, index=sector_return_momentum.index, columns=sector_return_momentum.columns)

        for date, momentum in sector_return_momentum.iterrows():
            valid_momentum = momentum.dropna()
            num_available_sectors = len(valid_momentum)
            num_selected_sectors = min(self.num_sectors, num_available_sectors // 2)
            if num_selected_sectors == 0:
                continue
            top_sectors = valid_momentum.nlargest(num_selected_sectors).index
            bottom_sectors = valid_momentum.nsmallest(num_selected_sectors).index

            top_presence_matrix.loc[date, top_sectors] = 1
            bottom_presence_matrix.loc[date, bottom_sectors] = 1

        # Calculate positions
        long_positions = top_presence_matrix.div(top_presence_matrix.sum(axis=1), axis=0).fillna(0)
        short_positions = -bottom_presence_matrix.div(bottom_presence_matrix.sum(axis=1), axis=0).fillna(0)

        # Apply invert options
        if self.invert_long:
            long_positions = -long_positions
        if self.invert_short:
            short_positions = -short_positions

        combined_positions = long_positions + short_positions

        # Store positions based on 'legs' parameter
        if self.legs == 'L':
            self.positions = long_positions
        elif self.legs == 'S':
            self.positions = short_positions
        elif self.legs == 'LS':
            self.positions = combined_positions
        elif self.legs == 'ALL':
            # Store all positions separately
            self.positions = {
                'Long': long_positions,
                'Short': short_positions,
                'Combined': combined_positions
            }
        else:
            raise ValueError(f"Invalid legs parameter '{self.legs}'.")

        # Store asset returns (sector average returns)
        self.asset_returns = sector_avg_returns.loc[spx500_returns.index]

        # Store presence matrices
        self.top_presence_matrix = top_presence_matrix
        self.bottom_presence_matrix = bottom_presence_matrix
        self.combined_presence_matrix = (top_presence_matrix + bottom_presence_matrix).clip(upper=1)

    def _determine_window_size(self):
        # Define a mapping from frequency to approximate number of periods per year
        freq_to_periods = {
            'D': 252,   # Trading days in a year
            'W': 52,    # Weeks in a year
            '2W': 26,   # Bi-weekly periods in a year
            'M': 12     # Months in a year
        }
        periods_per_year = freq_to_periods.get(self.trading_frequency)
        if not periods_per_year:
            raise ValueError("Invalid trading frequency.")

        # For an 11-month window, calculate the equivalent number of periods
        window_size = int((11 / 12) * periods_per_year)
        if window_size < 1:
            window_size = 1  # Ensure at least a window size of 1
        return window_size

    def get_signals(self):
        signals = {
            'asset_returns': self.asset_returns,
            'trading_frequency': self.trading_frequency
        }

        if self.legs == 'ALL':
            # Return all positions
            signals['positions'] = self.positions  # This is a dict with 'Long', 'Short', 'Combined'
        else:
            # Return the positions as 'positions'
            signals['positions'] = self.positions

        return signals

    def get_presence_matrix(self):
        if self.legs == 'L':
            return self.top_presence_matrix
        elif self.legs == 'S':
            return self.bottom_presence_matrix
        elif self.legs == 'LS':
            return self.combined_presence_matrix
        elif self.legs == 'ALL':
            return {
                'Long': self.top_presence_matrix,
                'Short': self.bottom_presence_matrix,
                'Combined': self.combined_presence_matrix
            }
        else:
            raise ValueError(f"Invalid legs parameter '{self.legs}'.")
