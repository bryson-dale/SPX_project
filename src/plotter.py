# plotter.py

import matplotlib.pyplot as plt

def plot_returns(returns_dict):
    plt.figure(figsize=(12, 6))
    for label, data in returns_dict.items():
        returns = data['returns']
        cumulative_returns = (1 + returns).cumprod()
        cumulative_returns /= cumulative_returns.iloc[0]
        plt.plot(cumulative_returns.index, cumulative_returns.values, label=label)
    plt.title('Strategy vs. Benchmark Returns')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns (Starting at 1)')
    plt.legend()
    plt.grid(True)
    plt.show()
