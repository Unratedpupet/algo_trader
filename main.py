import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

msft = yf.Ticker("MSFT")

historical_data = msft.history(period="1y")

# Calculating Moving Averages
# Creates a new column, with closing data with the mean of the rolling average of 50 days
historical_data['50_MA'] = historical_data['Close'].rolling(window=50).mean()
historical_data['200_MA'] = historical_data['Close'].rolling(window=200).mean()

historical_data['Signal'] = 0 # Initializes the signal column
# If 50 day MA crosses above 200 day MA, signal is 1
historical_data['Signal'][50:] = np.where(historical_data['50_MA'][50:] > historical_data['200_MA'][50:], 1, 0)

historical_data['Position'] = historical_data['Signal'].diff()

# Simple Backtest
historical_data['Market Return'] = historical_data['Close'].pct_change()
historical_data['Strategy Return'] = historical_data['Market Return'] * historical_data['Signal'].shift(1)

# In this plot, you'll see the buy signals marked with green upward-pointing triangles and the sell signals with red downward-pointing triangles.

plt.figure(figsize=(12,6))
plt.plot(historical_data['Close'], label='MSFT Close', alpha=0.5)
plt.plot(historical_data['50_MA'], label='50-Day MA', alpha=0.8)
plt.plot(historical_data['200_MA'], label='200-Day MA', alpha=0.8)
plt.plot(historical_data[historical_data['Position'] == 1].index, historical_data['50_MA'][historical_data['Position'] == 1], '^', markersize=10, color='g', lw=0, label='Buy Signal')
plt.plot(historical_data[historical_data['Position'] == -1].index, historical_data['50_MA'][historical_data['Position'] == -1], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
plt.title('MSFT Moving Average Crossover Strategy')
plt.legend()
plt.show()

# This will give you a visual representation of how well your strategy performed compared to just holding the asset.

historical_data['Cumulative Market Returns'] = (1 + historical_data['Market Return']).cumprod()
historical_data['Cumulative Strategy Returns'] = (1 + historical_data['Strategy Return']).cumprod()

plt.figure(figsize=(12,6))
plt.plot(historical_data['Cumulative Market Returns'], label='Market Returns')
plt.plot(historical_data['Cumulative Strategy Returns'], label='Strategy Returns')
plt.title('Market Returns vs Strategy Returns')
plt.legend()
plt.show()
