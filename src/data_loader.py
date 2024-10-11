# data_loader.py

import os
import pandas as pd
import numpy as np

class DataLoader:
    def __init__(self, data_folder='data'):
        self.data_folder = data_folder
        self.load_data()

    def load_data(self):
        # Check if the data folder exists
        if not os.path.exists(self.data_folder):
            raise FileNotFoundError(f"Data folder '{self.data_folder}' not found.")

        # Paths to data files
        permno_industry_map_path = os.path.join(self.data_folder, 'permno_industry_map.csv')
        spx_presence_path = os.path.join(self.data_folder, 'spx_presence.csv')
        spx_prices_path = os.path.join(self.data_folder, 'spx_prices.csv')

        # Load data
        self.permno_industry_map_raw = pd.read_csv(permno_industry_map_path)
        self.spx_presence_raw = pd.read_csv(spx_presence_path, index_col=0, parse_dates=True)
        self.spx_prices_raw = pd.read_csv(spx_prices_path, index_col=0, parse_dates=True)

        # Preprocess data
        self.preprocess_data()

    def preprocess_data(self):
        # Convert indices to datetime (already done during read_csv with parse_dates=True)

        # Ensure that permno columns are strings for consistent handling
        self.spx_prices_raw.columns = self.spx_prices_raw.columns.astype(str)
        self.spx_presence_raw.columns = self.spx_presence_raw.columns.astype(str)
        self.permno_industry_map_raw['permno'] = self.permno_industry_map_raw['permno'].astype(str)

        # Extend the presence matrix to match the prices, front-filling missing values
        date_range = pd.date_range(start=self.spx_prices_raw.index[0], end=self.spx_prices_raw.index[-1])
        self.spx_prices_raw = self.spx_prices_raw.reindex(date_range, method='ffill')
        self.spx_presence_raw = self.spx_presence_raw.reindex(date_range, method='ffill')

        # Sort the columns
        self.spx_prices_raw = self.spx_prices_raw.sort_index(axis=1)
        self.spx_presence_raw = self.spx_presence_raw.sort_index(axis=1)

        # Map permno to sector (hsiccd)
        permno_to_hsiccd = dict(zip(
            self.permno_industry_map_raw["permno"],
            self.permno_industry_map_raw["hsiccd"]
        ))

        # Create MultiIndex columns for prices
        hsiccd_header_prices = [permno_to_hsiccd.get(col, np.nan) for col in self.spx_prices_raw.columns]
        self.spx_prices_raw.columns = pd.MultiIndex.from_arrays(
            [self.spx_prices_raw.columns, hsiccd_header_prices],
            names=['permno', 'sector']
        )

        # Create MultiIndex columns for presence matrix
        hsiccd_header_presence = [permno_to_hsiccd.get(col, np.nan) for col in self.spx_presence_raw.columns]
        self.spx_presence_raw.columns = pd.MultiIndex.from_arrays(
            [self.spx_presence_raw.columns, hsiccd_header_presence],
            names=['permno', 'sector']
        )

        # Ensure that the columns in both DataFrames are the same and aligned
        common_columns = self.spx_prices_raw.columns.intersection(self.spx_presence_raw.columns)
        self.spx_prices_raw = self.spx_prices_raw[common_columns]
        self.spx_presence_raw = self.spx_presence_raw[common_columns]

    def get_prices(self):
        return self.spx_prices_raw

    def get_presence_matrix(self):
        return self.spx_presence_raw

    def get_permno_to_sector_map(self):
        return dict(zip(
            self.permno_industry_map_raw["permno"],
            self.permno_industry_map_raw["hsiccd"]
        ))
