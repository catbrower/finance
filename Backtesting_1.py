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
        self.HOLIDAYS = []

        with open('data/holidays.csv', 'r') as file:
            line = file.readline()
            while line:
                self.HOLIDAYS += [dateHelper.getDateAsDatetime(line.strip())]
                line = file.readline()

    def setCash(self, cash):
        self.initialCash = cash

    def isHoliday(self, date):
        date = dateHelper.getDateAsDatetime(date)
        return date in self.HOLIDAYS
            
    def run(self):
        date = dateHelper.getDateAsDatetime(self.startDate)
        endDate = dateHelper.getDateAsDatetime(self.endDate)
        provider = DataProvider()
        balance = BalancePortfolio(provider)
        broker = Broker(provider)
        broker.addCash(self.initialCash)
        portfolioValue = []

        while(date < endDate):
            date_str = dateHelper.getDateAsString(date)

            if(date.weekday() < 5 and not self.isHoliday(date)):
                value = broker.getValue(dateHelper.getDateAsString(date))

                if(self.lastRebalance > self.rebalanceDays):
                    self.lastRebalance = 0
                    broker.setPortfolio(balance.getPortfolio(date_str, value), date_str)
                else:
                    self.lastRebalance += 1

                portfolioValue += [[date, value]]
            date += timedelta(days = 1)

        # print(portfolioValue)
        with open('data/portfolioValue.csv', 'w') as file:
            for item in portfolioValue:
                date = dateHelper.getDateAsString(item[0])
                file.writelines(date + "," + str(item[1]) + "\n")

        print('Performance ' + self.startDate + ' - ' + self.endDate)
        print('Starting value: ' + str(self.initialCash))
        print('Final value: ' + str(portfolioValue[-1][1]))

backtester = BackTester('2017-01-01', '2018-01-02')
backtester.run()
