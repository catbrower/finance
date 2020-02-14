import sys
import pandas as pd
sys.path.append('/home/oem/Projects/Finance')

from DataProvider import DataProvider

def testOneStock():
    provider = DataProvider()

    provider.getData(['O'], '2018-01-02')
    assert provider.historyHasValues(['O'], '2018-01-02')   == True

    provider.getData(['O'], '2018-02-06')
    assert provider.historyHasValues(['O'], '2018-02-06')   == True
    assert provider.historyHasValues(['O'], '2018-01-04')   == False
    assert provider.historyHasValues(['XXX'], '2018-01-01') == False

#Dates provided when getting data from any class should be inclusive
def testDateRange():
    provider = DataProvider()
    provider.getData(['AMZN'], '2017-01-02', '2018-01-02')

    assert provider.history.empty == False

def testDateRangeOneStock():
    provider = DataProvider()
    provider.getData(['MSFT', 'XOM'], '2017-01-01', '2017-03-01')
    assert provider.historyHasValues(['MSFT'], '2018-02-01')        == False
    assert provider.historyHasValues(['MSFT', 'XOM'], '2018-02-01') == False
    assert provider.historyHasValues(['MSFT'], '2017-01-02')        == False

def testBadInputs():
    provider = DataProvider()
    try:
        provider.getData('sdfsf', 'sdfsdf')
    except:
        pass

    try:
        provider.getData([], 'dddddd', 'sdfsdfs')
    except:
        pass

    try:
        provider.getData(['MSFT'], '2018-02-01', '2018-01-01')
    except:
        pass
    