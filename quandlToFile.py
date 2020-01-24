import QuandlFetch
import sys

#pass args like so, dateFrom dateTo [tickers]

if(len(sys.argv) < 3):
    print('Incorrect arguments')
    print('Correct syntax is: python quandlToFile.py $startDate $endDate $ticker_1 ... $ticker_n')
    sys.exit()

try:
    dateFrom = sys.argv[1]
    dateTo = sys.argv[2]
    tickers = sys.argv[3::]

    data = QuandlFetch.getStocks(tickers, dateFrom, dateTo)
    data.to_csv('data/' + '_'.join(sys.argv[1::]) + '.csv')
    print('Data saved to: ' + 'data/' + '_'.join(sys.argv[1::]) + '.csv')
except:
    print('There was an error trying to parse arguments. Please ensure they are of the correct format')
    sys.exit()