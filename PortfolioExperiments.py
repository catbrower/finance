from threading import Lock, Thread
import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import QuandlFetch

stocks = ['HD', 'MSFT', 'O']
realEstateStocks = ['AIV', 'AMT', 'ARE', 'AVB', 'BXP', 'CBRE', 'CCI', 'DLR', 'DRE', 'EQIX', 'EQR', 'ESS', 'EXR', 'FRT', 'HST', 'IRM', 'KIM', 'MAA', 'MAC', 'O', 'PEAK', 'PLD', 'PSA', 'REG', 'SBAC', 'SLG', 'SPG', 'UDR', 'VNO', 'VTR', 'WELL', 'WY']
consDiscStocks = ['AAP', 'AMZN', 'APTV', 'AZO', 'BBY', 'BKNG', 'BWA', 'CCL', 'CMG', 'CPRI', 'DG', 'DHI', 'DLTR', 'DRI', 'EBAY', 'EXPE', 'F', 'GM', 'GPC', 'GPS', 'GRMN', 'HAS', 'HBI', 'HD', 'HLT', 'HOG', 'HRB', 'JWN', 'KMX', 'KSS', 'LB', 'LEG', 'LEN', 'LKQ', 'LOW', 'LVS', 'M', 'MAR', 'MCD', 'MGM', 'MHK', 'NCLH', 'NKE', 'NVR', 'NWL', 'ORLY', 'PHM', 'PVH', 'RCL', 'RL', 'ROST', 'SBUX', 'TGT', 'TIF', 'TJX', 'TPR', 'TSCO', 'UA', 'UAA', 'ULTA', 'VFC', 'WHR', 'WYNN', 'YUM']
energyStocks = ['APA', 'BKR', 'COG', 'COP', 'CVX', 'CXO', 'DVN', 'EOG', 'FANG', 'FTI', 'HAL', 'HES', 'HFC', 'HP', 'KMI', 'MPC', 'MRO', 'NBL', 'NOV', 'OKE', 'OXY', 'PSX', 'PXD', 'SLB', 'VLO', 'WMB', 'XEC', 'XOM']
financeStocks = ['AFL', 'AIG', 'AIZ', 'AJG', 'ALL', 'AMG', 'AMP', 'AON', 'AXP', 'BAC', 'BEN', 'BK', 'BLK', 'BRK.B', 'C', 'CB', 'CBOE', 'CFG', 'CINF', 'CMA', 'CME', 'COF', 'DFS', 'ETFC', 'FITB', 'FRC', 'GL', 'GS', 'HBAN', 'HIG', 'ICE', 'IVZ', 'JPM', 'KEY', 'L', 'LNC', 'MCO', 'MET', 'MKTX', 'MMC', 'MS', 'MSCI', 'MTB', 'NDAQ', 'NTRS', 'PBCT', 'PFG', 'PGR', 'PNC', 'PRU', 'RE', 'RF', 'RJF', 'SCHW', 'SIVB', 'SPGI', 'STT', 'SYF', 'TROW', 'TRV', 'UNM', 'USB', 'WFC', 'WLTW', 'ZION']
healthCareStocks = ['A', 'ABBV', 'ABC', 'ABMD', 'ABT', 'AGN', 'ALGN', 'ALXN', 'AMGN', 'ANTM', 'BAX', 'BDX', 'BIIB', 'BMY', 'BSX', 'CAH', 'CERN', 'CI', 'CNC', 'COO', 'CVS', 'DGX', 'DHR', 'DVA', 'EW', 'GILD', 'HCA', 'HOLX', 'HSIC', 'HUM', 'IDXX', 'ILMN', 'INCY', 'IQV', 'ISRG', 'JNJ', 'LH', 'LLY', 'MCK', 'MDT', 'MRK', 'MTD', 'MYL', 'PFE', 'PKI', 'PRGO', 'REGN', 'RMD', 'SYK', 'TFX', 'TMO', 'UHS', 'UNH', 'VAR', 'VRTX', 'WAT', 'WCG', 'XRAY', 'ZBH', 'ZTS']
industrialStocks = ['AAL', 'ALK', 'ALLE', 'AME', 'AOS', 'ARNC', 'BA', 'CAT', 'CHRW', 'CMI', 'CPRT', 'CSX', 'CTAS', 'DAL', 'DE', 'DOV', 'EFX', 'EMR', 'ETN', 'EXPD', 'FAST', 'FBHS', 'FDX', 'FLS', 'FTV', 'GD', 'GE', 'GWW', 'HII', 'HON', 'IEX', 'INFO', 'IR', 'ITW', 'JBHT', 'JCI', 'KSU', 'LHX', 'LMT', 'LUV', 'MAS', 'MMM', 'NLSN', 'NOC', 'NSC', 'PCAR', 'PH', 'PNR', 'PWR', 'RHI', 'ROK', 'ROL', 'ROP', 'RSG', 'RTN', 'SNA', 'SWK', 'TDG', 'TXT', 'UAL', 'UNP', 'UPS', 'URI', 'UTX', 'VRSK', 'WAB', 'WM', 'XYL']
infoTechStocks = ['AAPL', 'ACN', 'ADBE', 'ADI', 'ADP', 'ADS', 'ADSK', 'AKAM', 'AMAT', 'AMD', 'ANET', 'ANSS', 'APH', 'AVGO', 'BR', 'CDNS', 'CDW', 'CRM', 'CSCO', 'CTSH', 'CTXS', 'DXC', 'FFIV', 'FIS', 'FISV', 'FLIR', 'FLT', 'FTNT', 'GLW', 'GPN', 'HPE', 'HPQ', 'IBM', 'INTC', 'INTU', 'IPGP', 'IT', 'JKHY', 'JNPR', 'KEYS', 'KLAC', 'LDOS', 'LRCX', 'MA', 'MCHP', 'MSFT', 'MSI', 'MU', 'MXIM', 'NLOK', 'NOW', 'NTAP', 'NVDA', 'ORCL', 'PAYX', 'PYPL', 'QCOM', 'QRVO', 'SNPS', 'STX', 'SWKS', 'TEL', 'TXN', 'V', 'VRSN', 'WDC', 'WU', 'XLNX', 'XRX']
materialsStocks = ['ALB', 'AMCR', 'APD', 'AVY', 'BLL', 'CE', 'CF', 'CTVA', 'DD', 'DOW', 'ECL', 'EMN', 'FCX', 'FMC', 'IFF', 'IP', 'LIN', 'LYB', 'MLM', 'MOS', 'NEM', 'NUE', 'PKG', 'PPG', 'SEE', 'SHW', 'VMC', 'WRK']
communicationStocks = ['ATVI', 'CHTR', 'CMCSA', 'CTL', 'DIS', 'DISCA', 'DISCK', 'DISH', 'EA', 'FB', 'FOX', 'FOXA', 'GOOG', 'GOOGL', 'IPG', 'NFLX', 'NWS', 'NWSA', 'OMC', 'T', 'TMUS', 'TRIP', 'TTWO', 'TWTR', 'VIAC', 'VZ']
utilitiesStocks = ['AEE', 'AEP', 'AES', 'ATO', 'AWK', 'CMS', 'CNP', 'D', 'DTE', 'DUK', 'ED', 'EIX', 'ES', 'ETR', 'EVRG', 'EXC', 'FE', 'LNT', 'NEE', 'NI', 'NRG', 'PEG', 'PNW', 'PPL', 'SO', 'SRE', 'WEC', 'XEL']

allStocks = [realEstateStocks, consDiscStocks, energyStocks, financeStocks, healthCareStocks, industrialStocks, infoTechStocks, materialsStocks, communicationStocks, utilitiesStocks]
sectorPortfolios = []
sectorPortfolioLock = Lock()

def calcWeights(stocks):
    # Read in price data
    table = QuandlFetch.getStocks(stocks)

    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(table)
    S = risk_models.sample_cov(table)

    # Optimise for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    raw_weights = ef.max_sharpe()
    weights = ef.clean_weights()

    def f(x):
        return (x[1], weights[('adj_close', x[1])])

    def g(x):
        return weights[x]

    addSectorPortfolio([f(x) for x in weights if g(x) > 0])

def addSectorPortfolio(portfolio):
    global sectorPortfolios
    sectorPortfolioLock.acquire()
    sectorPortfolios += [x[0] for x in portfolio]
    sectorPortfolioLock.release()

threads = [Thread(target=calcWeights, args=([x])) for x in allStocks]
[x.start() for x in threads]
[x.join() for x in threads]


table = QuandlFetch.getStocks(sectorPortfolios)
mu = expected_returns.mean_historical_return(table)
S = risk_models.sample_cov(table)
ef = EfficientFrontier(mu, S)
raw_weights = ef.max_sharpe()
weights = ef.clean_weights()
ef.portfolio_performance(verbose=True)

print('Done')