import pandas as pd
import quandl
import numpy
import sys

quandl.ApiConfig.api_key = "www.quandl.com"
TICKER_LIMIT = 50

with open("quandl.key", "r") as f:
    quandl.ApiConfig.api_key = f.read().strip()

def get_data(path = "data/stock_prices.csv"):
    return pd.read_csv(path, parse_dates=True, index_col="date")

def getStocks(stockArray, startDate, endDate = None):
    if(len(stockArray) > TICKER_LIMIT):
        print("QuandlFetch.getStocks is limited to 50 stocks")
        sys.exit()

    endDate = startDate if endDate == None else endDate
    
    data = quandl.get_table('WIKI/PRICES', ticker = stockArray,
        qopts = { 'columns': ['date', 'ticker', 'adj_close'] },
        date = { 'gte': startDate, 'lte': endDate }, paginate=True)

    if(data.empty):
        return data
    else:
        df = data.set_index('date')
        df = df.pivot(columns='ticker')['adj_close']
        df.to_csv('data/tmp_data.csv')
        df = pd.read_csv('data/tmp_data.csv', parse_dates=True, index_col="date")
        return df