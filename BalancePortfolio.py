import csv
import sys
import pandas as pd
from threading import Lock, Thread
from datetime import datetime, timedelta

from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.efficient_frontier import EfficientFrontier

from DiscreteAllocation import DiscreteAllocation, get_latest_prices

import util
from DataProvider import DataProvider

GAMMA = 1
WEIGHT_BOUNDS = (0, 1)
ROUND_DIGITS = 4

class BalancePortfolio:
    def __init__(self):
        self.allStocks = []
        self.sectorPortfolios = []
        self.sectorPortfolioLock = Lock()
        self.dataProvider = DataProvider()
        self.lookbackDays = 90

        with open('data/snp500Tickers.csv', 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            self.allStocks = [row[1::] for row in csv_reader]

    def markowitz(self, data):
        mu = expected_returns.mean_historical_return(data)
        S = risk_models.sample_cov(data)
        return EfficientFrontier(mu, S, weight_bounds=WEIGHT_BOUNDS, gamma=GAMMA)

    def getWeights(self, ef):
        w = ef.max_sharpe()
        return {k: round(w[k], ROUND_DIGITS) for k in w if round(w[k], ROUND_DIGITS) > 0}

    def calcWeights(self, stocks, startDate, endDate):
        data = self.dataProvider.getData(stocks, startDate, endDate)
        ef = self.markowitz(data)
        weights = self.getWeights(ef)

        self.addSectorPortfolio([k for k in weights if weights[k] > 0])

    def addSectorPortfolio(self, portfolio):
        global sectorPortfolios
        self.sectorPortfolioLock.acquire()
        newTickers = [x for x in portfolio if x not in self.sectorPortfolios]
        self.sectorPortfolios += newTickers
        self.sectorPortfolioLock.release()

    #Quandl does not have data after 2018-03-07
    def getPortfolio(self, endDate):
        #Ensure dates are in correct format
        if(not util.isDateFormatCorrect(endDate)):
            util.printErrorAndDie('DataProvider.getData: start date is incorrect format')

        startDate = util.subtractDaysFromDate(endDate, self.lookbackDays)
        threads = [Thread(target=self.calcWeights, args=([x, startDate, endDate])) for x in self.allStocks]
        [x.start() for x in threads]
        [x.join() for x in threads]

        data = self.dataProvider.getData(self.sectorPortfolios, startDate, endDate)
        return self.markowitz(data)


#Scratch work

def get_data(path = "data/stock_prices.csv"):
    return pd.read_csv(path, parse_dates=True, index_col="date")

def test1():
    optimizer = BalancePortfolio()
    ef = optimizer.getPortfolio('2018-2-1')
    weights = optimizer.getWeights(ef)

    df = optimizer.dataProvider.history
    latest_prices = optimizer.dataProvider.getLatestPrices(stocks=weights.keys())

    try:
        da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=10000)
        allocation, leftover = da.lp_portfolio()
        print("Discrete Allocation:", allocation)
        print("Funds remaining: ${:.2f}".format(leftover))
        ef.portfolio_performance(verbose=True)
    except Exception as err:
        print(err)
        print(weights)
        print(latest_prices)
    
def test2():
    provider = DataProvider()
    df = provider.getData(['GOOG', 'AAPL', 'FB', 'BABA', 'AMZN', 'BBY', 'MA', 'PFE', 'SBUX'], '2017-1-1', '2018-1-1')

    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)
    ef = EfficientFrontier(mu, S)
    w = ef.max_sharpe()

    # latest_prices = get_latest_prices(df)
    latest_prices = provider.getLatestPrices()
    da = DiscreteAllocation(w, latest_prices)
    allocation, leftover = da.lp_portfolio()

test1()