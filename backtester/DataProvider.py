import math
import pandas as pd
import QuandlFetch

#it would be nice to add a way to stash all this to disk
class DataProvider:
    def __init__(self):
        self.history = None
        self.maxTickers = 25

    def getEmptyDataFrame(self):
        pass

    def retrieveDataFromWeb(self, stocks, startDate, endDate):
        dividedStocks = [stocks[x:x + self.maxTickers] for x in range(0, math.ceil(len(stocks) / self.maxTickers))]

        data = self.getEmptyDataFrame()
        data.reset_index()
        for group in dividedStocks:
            newData = QuandlFetch.getStocks(group, startDate, endDate).reset_index()
            data.merge(newData, how='right')

        self.history.reset_index()
        self.history.merge(data, how='right')
        self.history.set_index('date')
        data.set_index('date')

        return data

    #Type of date is unknown so just pass in whatever and try to convert it
    def dateToStr(self, date):
        try:
            return date.strftime("%Y:%m:%d")
        except:
            return date

    #index is not in columns, get it's name with df.index.name
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
