import quandl
import numpy

quandl.ApiConfig.api_key = "www.quandl.com"

with open("quandl.key", "r") as f:
    quandl.ApiConfig.api_key = f.read().strip()

def getStocks(stockArray, startDate = '2016-1-1', endDate = '2017-12-31' ):
    data = quandl.get_table('WIKI/PRICES', ticker = stockArray,
    qopts = { 'columns': ['date', 'ticker', 'adj_close'] },
    date = { 'gte': startDate, 'lte': endDate }, paginate=True)
    df = data.set_index('date')
    return df.pivot(columns='ticker')