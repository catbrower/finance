import DataProvider
import Controller
import Strategy

def getDataTest():
    provider = DataProvider.DataProvider()
    data = provider.getData(['MMM', 'XOM'], "2017-02-01")
    data = provider.getData(['MMM', 'XOM'], "2017-02-01")
    print('Data test passed')

    print('Data test failed')

#Run tests    
getDataTest()


