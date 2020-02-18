import pandas as pd

from util import dateHelper

def insertRow(df, index, value=None):
    return df.append(pd.DataFrame(index=[dateHelper.getDateAsString(index)]))

def getEmptyDataFrame():
    result = pd.DataFrame({'date': []})
    result = result.set_index('date')
    return result

#FIX this is hard coded for adj_close, as my program grows it's likely I'll need to generalize
def convertDataframe(df):
    if(df.empty):
        return getEmptyDataFrame()

    data = {}
    for column in df['adj_close'].columns:
        data[column] = df['adj_close'][column]

    data['date'] = df['adj_close'].index
    result = pd.DataFrame(data)
    result = result.set_index('date')
    return result

def combineDataFrames(df1, df2):
    if(not df1.empty and not df2.empty):
        try:
            if(df1.columns.intersection(df2.columns).empty):
                result = pd.concat([df1, df2], axis=1)
                return result
            else:
                return df1
                # dups = df1.columns.intersection(df2.columns)
                #df2 = df2.drop(dups)
                # return pd.concat([df1, df2], axis=1)
        except ValueError as err:
            print(err)
            return getEmptyDataFrame()
        except Exception as err:
            print(err)
            return getEmptyDataFrame()
    elif(not df1.empty):
        return df1
    elif(not df2.empty):
        return df2
    else:
        return getEmptyDataFrame()
