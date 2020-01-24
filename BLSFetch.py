import requests
import json

def convertMonth(month):
    if month == 'January': return '01'
    if month == 'February': return '02'
    if month == 'March': return '03'
    if month == 'April': return '04'
    if month == 'May': return '05'
    if month == 'June': return '06'
    if month == 'July': return '07'
    if month == 'August': return '08'
    if month == 'September': return '09'
    if month == 'October': return '10'
    if month == 'November': return '11'
    if month == 'December': return'12'

headers =['year', 'month', 'value']
dataSeries = ['CUUR0000SA0', 'SUUR0000SA0', 'PCUOMFG']
startYear = "2011"
endYear = "2014"

requestHeaders = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": dataSeries, "startyear" : startYear, "endyear" : endYear})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=requestHeaders)
json_data = json.loads(p.text)

for i in range(0, len(json_data['Results']['series'])):
    series = json_data['Results']['series'][i]
    with open('data/' + dataSeries[i] + '.csv', 'w') as f:
        f.write(','.join(headers) + '\n')
        for values in series['data']:
            f.write(','.join([values['year'], convertMonth(values['periodName']), values['value']]) + '\n')

#data format
#json_data.Results.series.[].data.[]