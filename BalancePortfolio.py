import csv
import sys
import pandas as pd
from datetime import datetime
from threading import Lock, Thread

from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation

from util import dateHelper, util
from DataProvider import DataProvider

GAMMA = 1
WEIGHT_BOUNDS = (0, 1)
ROUND_DIGITS = 4

class BalancePortfolio:
    def __init__(self, provider):
        self.allStocks = []
        self.sectorPortfolios = []
        self.sectorPortfolioLock = Lock()
        self.dataProvider = provider
        self.lookbackDays = 90

        with open('data/fastTest.csv', 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            self.allStocks = [row[1::] for row in csv_reader]

    def markowitz(self, data):
        mu = expected_returns.mean_historical_return(data)
        S = risk_models.sample_cov(data)
        return EfficientFrontier(mu, S, weight_bounds=WEIGHT_BOUNDS, gamma=GAMMA)

    def getWeights(self, ef):
        w = ef.max_sharpe()
        result = {k: round(w[k], ROUND_DIGITS) for k in w if round(w[k], ROUND_DIGITS)}
        return result

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
    def getPortfolio(self, endDate, value):
        #Ensure dates are in correct format
        if(not dateHelper.isDateFormatCorrect(endDate)):
            util.printErrorAndDie('DataProvider.getData: start date is incorrect format')

        startDate = dateHelper.subtractDaysFromDate(endDate, self.lookbackDays)
        threads = [Thread(target=self.calcWeights, args=([x, startDate, endDate])) for x in self.allStocks]
        [x.start() for x in threads]
        [x.join() for x in threads]

        data = self.dataProvider.getData(self.sectorPortfolios, startDate, endDate)
        
        weights = self.getWeights(self.markowitz(data))
        latest_prices = data.loc[endDate]
        da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=value)
        allocation, leftover = da.lp_portfolio()

        return pd.Series(allocation)