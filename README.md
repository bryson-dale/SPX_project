# SPX_class

A Python-based backtesting framework designed to analyze and simulate S&P 500 investment strategies. The project currently features a **Momentum Sector Long-Short Strategy** that uses historical sector data to calculate momentum and generate signals. The framework is modular, making it easy to add new strategies, benchmarks, and data sources.

## Project Structure

```plaintext
SPX_class/
│
├── data/                               # Folder containing CSV files with data used in the project
│   ├── spx_prices.csv                  # Daily prices of S&P 500 constituents (renamed from `spx_returns_cleaned`)
│   ├── permno_industry_map.csv         # Mapping of permno to industry codes
│   ├── permno_sic_map.csv              # Mapping of permno to SIC codes
│   ├── spx_presence.csv                # SPX presence matrix (whether a stock is in the index)
│   ├── ...
│
├── strategy/                           # Contains different strategy files
│   ├── __init__.py                     # Makes `strategy` a Python package for easy imports
│   ├── strategy_base.py                # Base class for strategy objects
│   ├── momentum_sector_LS.py           # Implements the momentum sector long-short strategy
│   └── your_new_strategy.py            # Placeholder for your new strategy
│
├── config.py                           # Configuration settings for the project
├── data_loader.py                      # Loads and preprocesses data from CSV files
├── benchmark.py                        # Code to calculate benchmark returns
├── backtest.py                         # Backtest logic for running the strategy
├── plotter.py                          # Plotting functions for results
├── stats_calculator.py                 # Statistics calculations for strategies
├── main.ipynb                          # Jupyter Notebook that runs the analysis
├── requirements.txt                    # List of dependencies required for the project
├── .gitignore                          # Specifies files and directories ignored by Git
├── README.md                           # Documentation for the project
└── environment.yml                     # Conda environment configuration (if using Conda)
```


## Installation

1. **Clone the Repository**:

   ```sh
   git clone https://github.com/your_username/SPX_class.git
   cd SPX_class
   ```

2. **Create a Virtual Environment** (Recommended):

   - **With venv**:

     ```sh
     python -m venv venv
     source venv/bin/activate  # On Linux/macOS
     venv\Scripts\activate     # On Windows
     ```

   - **With Conda** (Optional):

     ```sh
     conda env create -f environment.yml
     conda activate spx_class_env
     ```

3. **Install Dependencies**:

   - Using `requirements.txt`:

     ```sh
     pip install -r requirements.txt
     ```
4. **Data Preparation**

   Before running the backtesting framework, ensure that the `spx_returns_cleaned` file is added to the `data` folder. Once added, rename the file to `spx_prices.csv` to maintain consistency with the existing data structure and file references.

   ```plaintext
   SPX_class/
   │
   ├── data/
   │   ├── spx_prices.csv                  # Renamed file: formerly `spx_returns_cleaned`
   │   ├── ...


## Usage

### Running the Backtesting Framework

   To execute the backtesting analysis, run ```sh main.ipynb```. Plots and statistics are displayed at the bottom.

---


## **Adding a New Strategy**

One of the strengths of this framework is its modularity, allowing you to add new trading strategies easily. Below are detailed instructions on how to create and implement a new strategy within the existing framework.

### **Step 1: Create a New Strategy File**

1. **Navigate to the `strategy/` directory**:

   ```sh
   cd strategy
   ```

2. **Create a new Python file** for your strategy, e.g., `your_new_strategy.py`:

   ```sh
   touch your_new_strategy.py
   ```

3. **Implement your strategy class** in `your_new_strategy.py` by following the structure of the existing `strategy_base.py` and `momentum_sector_LS.py`.

### **Step 2: Implement the Strategy Class**

In your `your_new_strategy.py`, you need to:

1. **Import Necessary Modules**:

   ```python
   import pandas as pd
   import numpy as np
   from .strategy_base import Strategy
   ```

2. **Define Your Strategy Class**:

   ```python
   class YourNewStrategy(Strategy):
       def __init__(self, data_loader, config):
           self.data_loader = data_loader
           self.config = config
           self.set_parameters()
           # Initialize other necessary attributes
       
       def set_parameters(self, **kwargs):
           # Set default parameters and update with any provided kwargs
           self.parameter1 = kwargs.get('parameter1', default_value)
           self.parameter2 = kwargs.get('parameter2', default_value)
           # Add other parameters as needed
       
       def generate_signals(self):
           # Implement logic to generate trading signals
           pass
       
       def calculate_returns(self):
           # Implement logic to calculate strategy returns
           pass
       
       def get_results(self):
           # Return the results (returns and turnover)
           return {
               'returns': self.returns,
               'turnover': self.turnover,
               'trading_frequency': self.trading_frequency
           }
   ```

### **Step 3: Integrate Your Strategy into the Framework**

1. **In `main.ipynb` or your main script**, import your new strategy:

   ```python
   from strategy import YourNewStrategy
   ```

2. **Initialize the DataLoader and Config**:

   ```python
   from data_loader import DataLoader
   from config import Config

   data_loader = DataLoader(data_folder='data')
   config = Config(transaction_cost_bps=5)  # Set transaction costs as needed
   ```

3. **Initialize Your Strategy**:

   ```python
   strategy = YourNewStrategy(data_loader, config)
   strategy.set_parameters(
       parameter1=value1,
       parameter2=value2,
       trading_frequency='M',  # Use 'D', 'W', '2W', or 'M'
       start_date='YYYY-MM-DD',
       end_date='YYYY-MM-DD'
   )
   ```

4. **Initialize the Benchmark (Optional)**:

   ```python
   from benchmark import Benchmark
   benchmark = Benchmark(data_loader, config)
   ```

5. **Run the Backtest**:

   ```python
   from backtest import Backtest

   backtest = Backtest(strategy, benchmark)
   backtest.run_backtest()
   ```

6. **Retrieve and Analyze Results**:

   ```python
   # Get Returns
   returns_dict = backtest.get_returns()

   # Plot Returns
   from plotter import plot_returns
   plot_returns(returns_dict)

   # Display Statistics
   from stats_calculator import display_statistics
   display_statistics(returns_dict, sig_figs=4)
   ```

### **Step 4: Implement Required Methods**

Ensure your strategy class implements the following essential methods:

- **`set_parameters()`**: For setting strategy-specific parameters.
- **`generate_signals()`**: To generate trading signals based on your strategy logic.
- **`calculate_returns()`**: To compute the returns from the generated signals.
- **`get_results()`**: To return a dictionary containing returns, turnover, and trading frequency.

### **Detailed Code Updates Needed**

1. **In `your_new_strategy.py`**:

   - **Import necessary modules** (`pandas`, `numpy`, etc.).
   - **Define your strategy class** inheriting from `Strategy`.
   - **Implement the `__init__` method** to initialize attributes.
   - **Implement the `set_parameters` method** to set default and user-provided parameters.
   - **Implement the `generate_signals` method** with your strategy logic.
   - **Implement the `calculate_returns` method** to calculate returns based on signals.
   - **Implement the `get_results` method** to provide outputs compatible with the framework.

2. **In `strategy/__init__.py`**:

   - **Add an import statement** for your new strategy:
     ```python
     from .your_new_strategy import YourNewStrategy
     ```

3. **In `main.ipynb` or your main script**:

   - **Import your new strategy**:
     ```python
     from strategy import YourNewStrategy
     ```
   - **Initialize and set parameters** for your strategy.
   - **Integrate with the existing backtesting framework** as shown in the steps above.

### **Example of a Custom Strategy**

Here is a simplified example of what your `your_new_strategy.py` might look like:

```python
# strategy/your_new_strategy.py

import pandas as pd
import numpy as np
from .strategy_base import Strategy

class YourNewStrategy(Strategy):
    def __init__(self, data_loader, config):
        self.data_loader = data_loader
        self.config = config
        self.set_parameters()
        self.returns = None
        self.turnover = None
        self.trading_frequency = None

    def set_parameters(self, trading_frequency='M', start_date='1980-01-01', end_date=None):
        self.trading_frequency = trading_frequency.upper()
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date) if end_date else None

    def generate_signals(self):
        # Implement your signal generation logic here
        # For example, a simple moving average crossover
        prices = self.data_loader.get_prices()
        prices = prices.resample(self.trading_frequency).last()
        short_ma = prices.rolling(window=5).mean()
        long_ma = prices.rolling(window=20).mean()
        signals = (short_ma > long_ma).astype(int) - (short_ma < long_ma).astype(int)
        self.signals = signals

    def calculate_returns(self):
        # Calculate returns based on signals
        returns = self.data_loader.get_prices().pct_change()
        strategy_returns = (returns * self.signals.shift(1)).mean(axis=1)
        # Adjust for transaction costs and calculate turnover
        turnover = self.signals.diff().abs().sum(axis=1)
        transaction_costs = turnover * (self.config.transaction_cost_bps / 10000)
        strategy_returns -= transaction_costs
        self.returns = strategy_returns
        self.turnover = turnover

    def get_results(self):
        return {
            'returns': self.returns,
            'turnover': self.turnover,
            'trading_frequency': self.trading_frequency
        }
```
