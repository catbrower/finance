import pandas as pd
import numpy as np

class Broker:
    def __init__(self, provider):
        self.cash = 0
        self.portfolio = pd.Series({})
        self.provider = provider

    def setPortfolio(self, newStocks):
        diff = newStocks.combine(self.portfolio, np.subtract, fill_value=0)
        self.processOrders(diff)

    def addCash(self, cash):
        self.cash += cash

    #This will need to be filled in more to include
    def processOrders(self, orders):
        orders = orders.sort_values(ascending=True)
        self.portfolio = self.portfolio.combine(orders, np.add, fill_value=0)

    def getStocksInPortfolio(self):
        return [x for x in self.portfolio.keys()]

    def getValue(self, date):
        result = self.cash

        try:
            prices = self.provider.getData(self.getStocksInPortfolio(), date)
            prices = prices.loc[date]
            for value in self.portfolio.combine(prices, np.multiply):
                result += value
        except:
            pass

        return result