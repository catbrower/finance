from threading import Lock, Thread
import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import QuandlFetch
import csv

allStocks = []
sectorPortfolios = []
sectorPortfolioLock = Lock()

with open('data/snp500Tickers.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    allStocks = [row[1::] for row in csv_reader]

def calcWeights(stocks):
    # Read in price data
    table = QuandlFetch.getStocks(stocks)

    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(table)
    S = risk_models.sample_cov(table)

    # Optimise for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    raw_weights = ef.max_sharpe()
    weights = ef.clean_weights()

    def f(x):
        return (x[1], weights[('adj_close', x[1])])

    def g(x):
        return weights[x]

    addSectorPortfolio([f(x) for x in weights if g(x) > 0])

def addSectorPortfolio(portfolio):
    global sectorPortfolios
    sectorPortfolioLock.acquire()
    sectorPortfolios += [x[0] for x in portfolio]
    sectorPortfolioLock.release()

threads = [Thread(target=calcWeights, args=([x])) for x in allStocks]
[x.start() for x in threads]
[x.join() for x in threads]


table = QuandlFetch.getStocks(sectorPortfolios)
mu = expected_returns.mean_historical_return(table)
S = risk_models.sample_cov(table)
ef = EfficientFrontier(mu, S)
raw_weights = ef.max_sharpe()
weights = ef.clean_weights()
ef.portfolio_performance(verbose=True)

print('Done')