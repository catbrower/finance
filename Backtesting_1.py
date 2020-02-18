import pandas as pd
from datetime import datetime, timedelta

from util import dateHelper
from Broker import Broker
from DataProvider import DataProvider
from BalancePortfolio import BalancePortfolio

class BackTester:
    def __init__(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate
        self.rebalanceDays = 30
        self.lastRebalance = self.rebalanceDays + 1
        self.initialCash = 10000

    def setCash(self, cash):
        self.initialCash = cash
        
    def run(self):
        date = dateHelper.getDateAsDatetime(self.startDate)
        endDate = dateHelper.getDateAsDatetime(self.endDate)
        provider = DataProvider()
        balance = BalancePortfolio(provider)
        broker = Broker(provider)
        broker.addCash(self.initialCash)
        portfolioValue = []

        while(date < endDate):
            if date.weekday() < 5:
                if(self.lastRebalance > self.rebalanceDays):
                    self.lastRebalance = 0
                    broker.setPortfolio(balance.getPortfolio(dateHelper.getDateAsString(date)))
                else:
                    self.lastRebalance += 1

            portfolioValue += [[date, broker.getValue(dateHelper.getDateAsString(date))]]
            date += timedelta(days = 1)

        print(portfolioValue)

backtester = BackTester('2017-01-01', '2018-01-02')
backtester.run()
