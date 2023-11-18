import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Fetch historical data for Apple.
data = yf.download('AAPL', start='2020-01-01', end='2022-01-01')
# Calculate daily returns
data['Returns'] = data['Close'].pct_change()
# Create a binary column that indicates whether the price went up (1) or down (0)
data['Direction'] = np.where(data['Returns'] > 0, 1, 0)
# Drop any NaN values
data = data.dropna()

