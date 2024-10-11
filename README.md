# SPX_class

A Python-based backtesting framework designed to analyze and simulate S&P 500 investment strategies. The project currently features a **Momentum Sector Long-Short Strategy** that uses historical sector data to calculate momentum and generate signals. The framework is modular, making it easy to add new strategies, benchmarks, and data sources.

## Project Structure

```plaintext
SPX_class/
│
├── data/                               # Data folder containing CSV files
│   ├── permno_industry_map.csv
│   ├── permno_sic_map.csv
│   ├── spx_presence.csv
│   ├── spx_prices.csv
│
├── data_analysis/                      # Folder for analysis notebooks and scripts
│   ├── __init__.py
│   ├── beta_deciles.ipynb              # Notebook for analyzing beta deciles
│
├── src/                                # Main source code folder
│   ├── __init__.py
│   ├── config.py                       # Configuration settings for the project
│   ├── data_loader.py                  # Code for loading data from the `data` folder
│   ├── benchmark.py                    # Code to calculate benchmark returns
│   ├── backtest.py                     # Backtest logic for running the strategy
│   ├── plotter.py                      # Plotting functions for results
│   ├── stats_calculator.py             # Statistics calculations for strategies
│   ├── strategy/                       # Folder containing strategy code
│   │   ├── __init__.py
│   │   ├── strategy_base.py
│   │   ├── momentum_sector_LS.py
│
├── main.ipynb                          # Main Jupyter Notebook for running the code and backtests
│
├── .gitignore                          # Git ignore file for excluding files from GitHub
├── README.md                           # Documentation for the project
├── requirements.txt                    # List of Python dependencies
└── environment.yml                     # Conda environment file (optional, if using Conda)

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

