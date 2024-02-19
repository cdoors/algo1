import numpy as np
from sklearn.linear_model import LinearRegression
import yfinance as yf
import pandas as pd

# Ensure the correct path to your CSV file
df = pd.read_csv('sp500_clustered.csv', parse_dates=['date'], index_col=['date', 'ticker'])

end_date = '2024-02-01'
start_date = pd.to_datetime(end_date) - pd.DateOffset(years=5)

# Load SPY data (assuming you have it or fetch it similarly as your stock data)
spy_data = yf.download('SPY', start=start_date, end=end_date)['Adj Close'].pct_change().fillna(0)

# Prepare for beta calculation
betas = {}

# Iterate through each stock to calculate its beta relative to SPY
for ticker in df.index.get_level_values('ticker').unique():
    stock_returns = df.loc[(slice(None), ticker), :]['adj close'].pct_change().fillna(0)
    
    # Align SPY data with stock returns based on dates
    spy_aligned = spy_data.reindex(stock_returns.index.get_level_values('date'))
    
    # Linear regression to find beta
    model = LinearRegression().fit(spy_aligned.values.reshape(-1, 1), stock_returns.values)
    
    # The coefficient (slope) is the beta
    betas[ticker] = model.coef_[0]

# Example: Add beta values to your DataFrame (optional, for illustrative purposes)
# This step depends on how you intend to use the betas in your analysis
for ticker in betas:
    df.loc[df.index.get_level_values('ticker') == ticker, 'beta'] = betas[ticker]

# Save or proceed with the analysis
df.to_csv('betas_added.csv')
