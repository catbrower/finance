import math
import pandas as pd
from threading import Lock, Thread

import util
import QuandlFetch

#it would be nice to add a way to stash all this to disk
class DataProvider:
    def __init__(self):
        self.historyLock = Lock()
        self.history = util.getEmptyDataFrame()
        self.maxTickers = 25

    def setHistory(self, newHistory):
        global history
        self.historyLock.acquire()
        if(newHistory is None):
            #Something broke
            print('DataProvider.setHistory: there was an error setting history')
        else:
            self.history = newHistory
        self.historyLock.release()

    def retrieveDataFromWeb(self, stocks, startDate, endDate):
        dividedStocks = [stocks[x:x + self.maxTickers] for x in range(0, math.ceil(len(stocks) / self.maxTickers))]
        data = pd.DataFrame()

        for group in dividedStocks:
            data = util.combineDataFrames(data, QuandlFetch.getStocks(group, startDate, endDate))
            self.setHistory(util.combineDataFrames(self.history, data))

        return data

    #Row should be a date, and columns tickers
    def historyHasValues(self, tickers, startDate, endDate = None):
        if(self.history.empty):
            return False

        if(endDate == None):
            try:
                self.history.loc[startDate][tickers]
                return True
            except:
                return False
        else:
            try:
                return len(self.history.loc[startDate:endDate][tickers]) == util.getDaysInRange(startDate, endDate)
            except:
                return False

    #stocks can optionally be passed in
    #this sometimes returns NaNs
    def getLatestPrices(self, stocks=[]):
        # latest = get_latest_prices(self.history)
        index = self.history.index.max

        if(stocks and len(stocks) < 1):
            result = self.history.loc[index]
        else:
            result = self.history.loc[index][stocks]

        return result

    #I'm not reall sure how this data is stored...
    def getData(self, stocks, startDate, endDate = None):
        #Ensure dates are in correct format
        if(not util.isDateFormatCorrect(startDate)):
            util.printErrorAndDie('DataProvider.getData: start date is incorrect format')

        if((not endDate == None) and (not util.isDateFormatCorrect(startDate))):
            util.printErrorAndDie('DataProvider.getData: end date is incorrect format')

        if(endDate == None):
            #First check if data exists in history and return that, else
            #get new data from web and store it in history
            if(self.historyHasValues(startDate, stocks)):
                return self.history.loc[startDate][stocks]
            else:
                return self.retrieveDataFromWeb(stocks, startDate, startDate)
        else:
            endDateStr = util.getDateAsString(endDate)
            if(self.historyHasValues([startDate, endDate], stocks)):
                return self.history.loc[startDate, endDateStr][stocks]
            else:
                return self.retrieveDataFromWeb(stocks, startDate, endDateStr)

