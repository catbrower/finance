from datetime import datetime, timedelta
from threading import Lock, Thread
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import csv
import numpy as np
import pandas as pd
import QuandlFetch
import DataProvider

class Strategy:
    def __init__(self):
        self.rebalanceDays = 30
        self.lastRebalance = None
        self.lookBackDays = 90
        self.allStocks = []
        self.portfolio = []
        self.stockData = None
        self.data = DataProvider.DataProvider()

        with open('data/snp500Tickers.csv', 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            self.allStocks = [row[1::] for row in csv_reader]

    def setTimePeriod(self, startDate, endDate):
        newStartDate = startDate - timedelta(days = self.lookBackDays)
        self.data.retrieveDataFromWeb([x for y in self.allStocks for x in y], newStartDate, endDate)

    def rebalance(self, date):
        sectorPortfolios = []
        sectorPortfolioLock = Lock()

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
                return (x[1], weights[('adj_close', x[1])], )

            def g(x):
                return weights[x]

            return [f(x) for x in weights if g(x) > 0]

        def calcWeightsThread(stocks, sectorPortfolios):
            portfolio = calcWeights(stocks)

            sectorPortfolioLock.acquire()
            sectorPortfolios += [stockTuple[0] for stockTuple in portfolio]
            sectorPortfolioLock.release()

        threads = [Thread(target=calcWeightsThread, args=([industryStocks], sectorPortfolios)) for industryStocks in self.allStocks]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        self.portfolio = calcWeights(sectorPortfolios)
        self.lastRebalance = date

    def processTick(self, date):
        if(self.lastRebalance == None):
            self.rebalance(date)
        elif((date - self.lastRebalance).days >= self.rebalanceDays):
            self.rebalance(date)

        #attach current stock prices
        results = [(x[0], x[1]) for x in self.portfolio]
            
        return self.portfolio
