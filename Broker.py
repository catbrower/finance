import math
import numpy as np
import pandas as pd

class Broker:
    def __init__(self, provider):
        self.cash = 0
        self.portfolio = pd.Series({})
        self.provider = provider

    def setPortfolio(self, newStocks, date):
        diff = newStocks.combine(self.portfolio, np.subtract, fill_value=0)
        self.processOrders(diff, date)

    def addCash(self, cash):
        self.cash += cash

    def sell(self, ticker, qty, date):
        self.portfolio[ticker] -= qty
        price = self.provider.getData([ticker], date).loc[date][ticker]
        self.cash += qty * price

    def buy(self, ticker, qty, date):
        if(ticker in self.portfolio):
            self.portfolio[ticker] += qty
        else:
            self.portfolio[ticker] = qty

        price = self.provider.getData([ticker], date).loc[date][ticker]

        self.cash -= qty * price

    #This will need to be filled in more to include
    def processOrders(self, orders, date):
        orders = orders.sort_values(ascending=True)
        # tickers = [x for x in pd.Series(self.getStocksInPortfolio()).combine(orders, max, fill_value=0).keys()]
        # prices = self.provider.getData(tickers, date).loc[date]

        for ticker in orders.keys():
            if(orders[ticker] < 0):
                self.sell(ticker, abs(orders[ticker]), date)
            else:
                self.buy(ticker, abs(orders[ticker]), date)

        # self.portfolio = self.portfolio.combine(orders, np.add, fill_value=0)

    def getStocksInPortfolio(self):
        return [x for x in self.portfolio.keys()]

    def getValue(self, date):
        result = self.cash

        if(len(self.portfolio) > 0):
            try:
                stocks = self.getStocksInPortfolio()
                prices = self.provider.getData(stocks, date)
                prices = prices.loc[date]
            
                for value in self.portfolio.combine(prices, np.multiply):
                    result += value
            except Exception as err:
                #check values here
                p = self.portfolio
                pass

        return round(result, 2)