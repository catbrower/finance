import pandas as pd

class StockData():
    def __init__(self):
        self.data = []
        self.columns = []

    def addDataFrame(self, dataFrame):
        newData = dataFrame.values
        newColumns = dataFrame.columns

        if 'date' not in newColumns:
            raise 'The new data must contain a date column'

        columnsToAdd = [newColumns.index(x) for x in newColumns if x not in self.columns]
        for i in columnsToAdd:
            self.columns.append(newColumns[i])


#getRow is calls loc[]
df1 = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': ['b1', 'b2', 'b3', 'b4', 'b5']})
df2 = pd.DataFrame({'A': [1, 2, 3, 6, 7], 'B': ['b6', 'b7', 'b8', 'b9', 'b10'], 'C': ['c1', 'c2', 'c3', 'c4', 'c5']})
df1.set_index('A', inplace=True)
df2.set_index('A', inplace=True)

#rows with same index
rows = df2.loc[df1.index].dropna()

#pd.concat([frames], axis=1) this can combine them but doesn't override columns