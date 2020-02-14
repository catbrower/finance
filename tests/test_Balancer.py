import sys
import pandas as pd
sys.path.append('/home/oem/Projects/Finance')

from BalancePortfolio import BalancePortfolio

def test_sectorPortfolios():
    date = '2018-01-02'
    optimizer = BalancePortfolio()
    optimizer.calcWeights(['AIV', 'AMT', 'ARE', 'AVB', 'BXP'], date, date)


# test_sectorPortfolios()