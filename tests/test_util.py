import sys
import pandas as pd
from datetime import datetime
sys.path.append('/home/oem/Projects/Finance')

import util
import QuandlFetch

DATE_FORMAT = '%Y-%m-%d'
SAMPLE_STOCKS = ['GOOG', 'AAPL', 'FB', 'BABA', 'AMZN', 'BBY', 'MA', 'PFE', 'SBUX']

def test_getDateAsDatetime():
    result = util.getDateAsDatetime('2020-01-01')
    assert isinstance(result, datetime)

    result = util.getDateAsDatetime(result)
    assert isinstance(result, datetime)

def test_getDateAsString():
    result = util.getDateAsString(datetime.strptime('2020-01-01', DATE_FORMAT))
    assert type(result) == str

    result = util.getDateAsString(result)
    assert type(result) == str

def test_isDateFormatCorrect():
    assert util.isDateFormatCorrect('2020-01-01') == True
    assert util.isDateFormatCorrect(124) == False

def test_getDaysInRange():
    assert util.getDaysInRange('2020-01-01', '2020-01-20') == 20
    assert util.getDaysInRange('2020-01-01', '2020-01-01') == 1

def subtractDaysFromDate():
    assert util.subtractDaysFromDate('2020-01-02', 1) == '2020-01-01'

def test_getDateRange():
    dates = util.getDateRange('2020-01-01', '2020-01-05')
    assert len(dates) == 5
    assert dates[0] == '2020-01-01'
    assert dates[1] == '2020-01-02'
    assert dates[2] == '2020-01-03'
    assert dates[3] == '2020-01-04'
    assert dates[4] == '2020-01-05'

def test_convertDataFrame():
    df = QuandlFetch.getStocks(SAMPLE_STOCKS, '2017-01-01', '2018-01-01')
    result = util.convertDataframe(df)

def test_insertRow():
    pass

def test_combineDataFrames():
    pass
