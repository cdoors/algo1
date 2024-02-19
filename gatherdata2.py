import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
import pandas_ta as ta
import warnings

# Load S&P 500 companies list
sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S&P_500_companies')[0]
sp500['Symbol'] = sp500['Symbol'].str.replace('.', '-')

symbols_list = sp500['Symbol'].unique().tolist()

end_date = '2024-02-01'
start_date = pd.to_datetime(end_date) - pd.DateOffset(years=5)

# Download data and use future_stack=True to adopt the new implementation
df = yf.download(tickers=symbols_list, start=start_date, end=end_date).stack(future_stack=True)

df.index.names = ['date', 'ticker']
df.columns = df.columns.str.lower()

# Calculate the previous day's close price change as a percentage
# It's better to avoid inplace=True to address the warning and ensure direct assignment
df = df.assign(prev_day_change=df.groupby(level='ticker')['adj close'].pct_change() * 100)

# Fill NaN values that result from calculating percentage change
df['prev_day_change'] = df['prev_day_change'].fillna(0)

# Calculate MACD using pandas_ta directly on the DataFrame
macd = ta.macd(df['adj close'], fast=12, slow=26, signal=9)
df = df.assign(MACD=macd['MACD_12_26_9'], MACD_signal=macd['MACDs_12_26_9'], MACD_hist=macd['MACDh_12_26_9'])

# Drop NaN values in a new DataFrame to ensure clean data
df_clean = df.dropna()

# Save the clean DataFrame to CSV
df_clean.to_csv('sp500.csv')
