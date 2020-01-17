from datetime import datetime, timedelta
from threading import Lock, Thread
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import csv
import numpy as np
import pandas as pd
import QuandlFetch

class OderApi:
    def ___init___(self):
        self.slippage_std = .01
        self.prob_of_failure = 0 #.0001
        self.fee = .02
        self.fixed_fee = 10
        self.calculate_fee = lambda x: self.fee * abs(x) + self.fixed_fee

    def process_order(self, order):
        slippage = np.random.normal(0, self.slippage_std, size=1)[0]

        if(np.random.choice([False, True], p=[self.prob_of_failure, 1 - self.prob_of_failure], size=1)[0]):
            trade_fee = self.fee * order[1] * (1 + slippage) * order[2]
            return (order[0], order[1] * (1 + slippage), order[2], self.calculate_fee(trade_fee))

#it would be nice to add a way to stash all this to disk
class DataProvider:
    def __init__(self):
        self.history = pd.DataFrame()

    def retrieveDataFromWeb(self, stocks, startDate, endDate):
        data = QuandlFetch.getStocks(stocks, startDate, endDate)
        
        #have to provide columns?
        # self.history.merge(data)

        return data

    #Type of date is unknown so just pass in whatever and try to convert it
    def dateToStr(self, date):
        try:
            return date.strftime("%Y:%m:%d")
        except:
            return date

    def historyHasColumns(self, names):
        return set(names).issubset(self.history.columns)

    def historyHasRows(self, rowIds):
        try:
            for id in rowIds:
                if(len(self.history.loc[id]) < 1):
                    return False
        except:
            return False

        return True

    def historyHasValues(self, rows, columns):
        hasRows = self.historyHasRows(rows)
        hasCols = self.historyHasColumns(columns)
        return hasRows and hasCols

    #I'm not reall sure how this data is stored...
    def getData(self, stocks, startDate, endDate = None):
        startDateStr = self.dateToStr(startDate)
        if(endDate == None):
            #First check if data exists in history and return that, else
            #get new data from web and store it in history
            if(self.historyHasValues([startDate], stocks)):
                return self.history.loc[startDateStr]
            else:
                return self.retrieveDataFromWeb(stocks, startDateStr, startDateStr)
        else:
            endDateStr = self.dateToStr(endDate)
            hasData = False
            if(hasData):
                return self.history[startDateStr:endDateStr]
            else:
                return self.retrieveDataFromWeb(stocks, startDateStr, endDateStr)


class Strategy:
    def __init__(self):
        self.rebalanceDays = 30
        self.lastRebalance = None
        self.lookBackDays = 90
        self.allStocks = []
        self.portfolio = []
        self.stockData = None
        self.data = DataProvider()

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

class Controller:
    def __init__(self, startDate, endDate, strategy):
        self.startDate = datetime.strptime(startDate, '%Y-%m-%d')
        self.nowDate = datetime.strptime(startDate, '%Y-%m-%d')
        self.endDate = datetime.strptime(endDate, '%Y-%m-%d')
        self.strategy = strategy
        self.history = []
        self.strategy.setTimePeriod(self.startDate, self.endDate)

    #for now hard code to tick one day at a time
    #Keep this as a seperate func since logic will be more
    #complex later on
    def advanceTime(self):
        self.nowDate = self.nowDate + timedelta(days=1)

    def begin(self):
        while(self.nowDate < self.endDate):
            currentStocks = self.strategy.processTick(self.nowDate)
            self.history += [currentStocks]
            print(currentStocks)
            self.advanceTime()

# strategy = Strategy()
# controller = Controller('2019-01-01', '2020-01-01', strategy)
# controller.begin()

provider = DataProvider()
data = provider.getData(['MMM', 'XOM'], "2017-02-01")
data = provider.getData(['MMM', 'XOM'], "2017-02-01")
print(data)