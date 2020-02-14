import sys
from datetime import datetime, timedelta
import pandas as pd

DATE_FORMAT = '%Y-%m-%d'

def getDateAsDatetime(date):
    if(isinstance(date, datetime)):
        return date

    return datetime.strptime(date, DATE_FORMAT)

def getDateAsString(date):
    if(type(date) == str):
        return date
        
    return date.strftime(DATE_FORMAT)

def isDateFormatCorrect(date):
    return type(date) == str

def getDaysInRange(date1, date2, inclusive=True):
    days = (getDateAsDatetime(date2) - getDateAsDatetime(date1)).days
    return days + 1 if inclusive else days

def subtractDaysFromDate(date, days):
    if(isDateFormatCorrect(date)):
        newDate = datetime.strptime(date, DATE_FORMAT) - timedelta(days = days)
        return getDateAsString(newDate)
    else:
        print('util.subtractDaysFromDate: provided date is in incorrect format')
        sys.exit()

def getDateRange(startDate, endDate):
    startDate = getDateAsDatetime(startDate)
    endDate = getDateAsDatetime(endDate)
    currentDate = startDate
    result = []
    
    while(currentDate <= endDate):
        result += [getDateAsString(currentDate)]
        currentDate += timedelta(days=1)

    return result

#Fix add the ability to insert data instead of just initializing it
#Also, is there a way to do an implace insert? Using insert returns a new
#DF it doesn't alter it
def insertRow(df, index, value=None):
    return df.append(pd.DataFrame(index=[getDateAsString(index)]))

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

def printErrorAndDie(error):
    print(error)
    sys.exit()