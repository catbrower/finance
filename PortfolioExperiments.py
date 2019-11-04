import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import QuandlFetch

stocks = ['AAPL','AMZN','GOOGL', 'O', 'MMM', 'QQQ']

# Read in price data
table = QuandlFetch.getStocks(stocks)

# Calculate expected returns and sample covariance
mu = expected_returns.mean_historical_return(table)
S = risk_models.sample_cov(table)

# Optimise for maximal Sharpe ratio
ef = EfficientFrontier(mu, S)
raw_weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
print(cleaned_weights)
ef.portfolio_performance(verbose=True)