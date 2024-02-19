import pandas as pd

# Load your data with betas
df = pd.read_csv('betas_added.csv', parse_dates=['date'], index_col=['date', 'ticker'])

# Convert daily data to monthly data
# This example calculates monthly returns, adjust as necessary for your dataset
monthly_returns = df.groupby('ticker').resample('M')['adj close'].last().pct_change()

# Reset index to work with data easily afterward
monthly_returns = monthly_returns.reset_index()

df.to_csv('monthlysp500.csv')
