import pandas_datareader as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
import pandas_ta as ta
import warnings

sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S&P_500_companies')[0]

sp500['Symbol'] = sp500['Symbol'].str.replace('.','-')

symbols_list = sp500['Symbol'].unique().tolist()

end_date = '2024-02-01'

start_date = pd.to_datetime(end_date)-pd.DateOffset(365*5)

df = yf.download(tickers=symbols_list,start=start_date,end=end_date).stack()

df.index.names = ['date','ticker']

df.columns = df.columns.str.lower()

# Calculate the previous day's close price change as a percentage
df['prev_day_change'] = df.groupby(level='ticker')['adj close'].pct_change() * 100

# Handle NaN values that result from calculating percentage change
df['prev_day_change'].fillna(0, inplace=True)

# Calculate MACD using pandas_ta
import pandas as pd
import pandas_ta as ta

# Assuming you've already loaded your DataFrame 'df' and it has a 'close' column
df['MACD'] = ta.macd(df['adj close'], fast=12, slow=26, signal=9)['MACD_12_26_9']
df['MACD_signal'] = ta.macd(df['adj close'], fast=12, slow=26, signal=9)['MACDs_12_26_9']
df['MACD_hist'] = ta.macd(df['adj close'], fast=12, slow=26, signal=9)['MACDh_12_26_9']


# Handling possible NaN values that might be introduced during the calculation
df.dropna(inplace=True)

# Now, your DataFrame 'df' includes MACD features: MACD line, signal line, and MACD histogram.

df.to_csv('sp500.csv')
