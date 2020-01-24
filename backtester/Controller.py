from datetime import datetime, timedelta

class Controller:
    def __init__(self, startDate, endDate, strategy):
        self.startDate = datetime.strptime(startDate, '%Y-%m-%d')
        self.nowDate = datetime.strptime(startDate, '%Y-%m-%d')
        self.endDate = datetime.strptime(endDate, '%Y-%m-%d')
        self.strategy = strategy
        self.history = []
        self.strategy.setTimePeriod(self.startDate, self.endDate)

    #for now hard code to tick one day at a time
    #Keep this as a seperate func since logic will be more
    #complex later on
    def advanceTime(self):
        self.nowDate = self.nowDate + timedelta(days=1)

    def begin(self):
        while(self.nowDate < self.endDate):
            currentStocks = self.strategy.processTick(self.nowDate)
            self.history += [currentStocks]
            print(currentStocks)
            self.advanceTime()