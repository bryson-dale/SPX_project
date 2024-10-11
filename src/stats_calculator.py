# stats_calculator.py

import pandas as pd
from scipy.stats import skew
import numpy as np
from IPython.display import display, HTML

def calculate_turnover(positions):
    """
    Calculate the turnover of a strategy based on its positions.
    
    Parameters:
        positions (pd.DataFrame): DataFrame where rows are time periods and columns are assets.
                                   Values indicate the position size (e.g., weights).
    
    Returns:
        pd.Series: A Series representing the turnover for each period.
    """
    turnover = positions.diff().abs().sum(axis=1)
    turnover.iloc[0] = positions.iloc[0].abs().sum()
    return turnover

def calculate_statistics(returns, turnover=None, trading_frequency='M', presence=None):
    """
    Calculate various statistical metrics for a given series of returns.
    
    Parameters:
        returns (pd.Series): Series of strategy returns.
        turnover (pd.Series, optional): Series of turnover values.
        trading_frequency (str): Frequency of trading periods ('D', 'W', 'M', etc.).
        presence (pd.Series or pd.DataFrame, optional): Presence matrix indicating active periods.
    
    Returns:
        dict: Dictionary containing calculated statistics.
    """
    # Filter returns based on presence matrix if provided
    if presence is not None:
        # Ensure presence index aligns with returns index
        presence = presence.reindex(returns.index)
        # Create a mask where at least one position is held
        if isinstance(presence, pd.DataFrame):
            active_periods = presence.sum(axis=1) > 0
        else:
            active_periods = presence > 0
        # Filter returns and turnover
        returns = returns[active_periods]
        if turnover is not None:
            turnover = turnover[active_periods]
    
    stats = {}
    # Determine periods per year based on trading frequency
    freq_map = {
        'D': 252,
        'W': 52,
        '2W': 26,
        'M': 12
    }
    periods_per_year = freq_map.get(trading_frequency.upper())
    if not periods_per_year:
        raise ValueError("Invalid trading frequency.")
    
    # Annualized Geometric Return
    total_return = (1 + returns).prod()
    num_periods = len(returns)
    num_years = num_periods / periods_per_year
    if num_years == 0:
        annualized_return = 0
    else:
        annualized_return = total_return ** (1 / num_years) - 1
    stats['Annualized Return (%)'] = annualized_return * 100
    
    # Annualized Standard Deviation
    annualized_std = returns.std() * np.sqrt(periods_per_year)
    
    # Annualized Sharpe Ratio (Assuming risk-free rate = 0)
    sharpe_ratio = annualized_return / annualized_std if annualized_std != 0 else np.nan
    stats['Annualized Sharpe Ratio'] = sharpe_ratio
    
    # Skewness
    stats['Skewness'] = skew(returns)
    
    # Maximum Drawdown
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()
    stats['Max Drawdown (%)'] = max_drawdown * 100
    
    # Average Turnover
    if turnover is not None:
        avg_turnover = turnover.mean()
        stats['Average Turnover (%)'] = avg_turnover * 100
    else:
        stats['Average Turnover (%)'] = np.nan
    
    return stats

def display_statistics(returns_dict, strategies, sig_figs=4):
    """
    Display statistical metrics for all strategies in an HTML table.
    
    Parameters:
        returns_dict (dict): Dictionary containing returns and turnover for each strategy.
        strategies (list): List of strategy instances.
        sig_figs (int): Number of significant figures for rounding.
    """
    def format_sig_figs(x):
        if x == 0 or not np.isfinite(x):
            return '0'
        else:
            return '{0:.{1}g}'.format(x, sig_figs)
    
    stats_list = []
    for label, data in returns_dict.items():
        returns = data['returns']
        turnover = data.get('turnover', None)
        trading_freq = data.get('trading_frequency', 'M')
        
        # Find the corresponding strategy
        strategy = next((s for s in strategies if s.name in label), None)
        presence = None
        if strategy:
            # Extract the leg from the label
            if ' - ' in label:
                leg = label.split(' - ')[-1]
                presence_matrix = strategy.get_presence_matrix()
                if isinstance(presence_matrix, dict) and leg in presence_matrix:
                    presence = presence_matrix[leg]
                elif isinstance(presence_matrix, pd.DataFrame):
                    presence = presence_matrix
        # Calculate statistics
        stats = calculate_statistics(returns, turnover, trading_frequency=trading_freq, presence=presence)
        stats['Strategy'] = label
        stats_list.append(stats)
    
    stats_df = pd.DataFrame(stats_list).set_index('Strategy')
    
    # Apply the significant figures formatting
    stats_df = stats_df.applymap(format_sig_figs)
    
    # Display the DataFrame in HTML format
    display(HTML(stats_df.to_html(escape=False)))
