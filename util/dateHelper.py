import sys
from datetime import datetime, timedelta

DATE_FORMAT = '%Y-%m-%d'
HOLIDAYS = []

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