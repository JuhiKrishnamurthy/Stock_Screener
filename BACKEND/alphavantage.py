import sys
import requests
import time

API_KEY='K756X9YKTO7JWDJ5'
MAX_TRIES=10
SLEEP_TIME=60

def time_series_daily(symbol,outputsize='compact'):
    n = 0
    while (n <MAX_TRIES):
        n += 1
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&'+\
            'symbol='+symbol +'&outputsize='+outputsize+'&apikey='+API_KEY
        r = requests.get(url)
        data = r.json()
        if( ("Note" in data) and ("Thank you" in data["Note"])):
                time.sleep(SLEEP_TIME)
                data={}
        else:
            return data
    return data


def time_series_weekly(symbol):
    n = 0
    while (n <MAX_TRIES):
        n += 1
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&'+\
            'symbol='+symbol +'&apikey='+API_KEY
        r = requests.get(url)
        data = r.json()
        if( ("Note" in data) and ("Thank you" in data["Note"])):
            time.sleep(SLEEP_TIME)
            data ={}
        else:
            return data
    return data
    

def time_series_weekly_adjusted(symbol):
    n = 0
    while (n <MAX_TRIES):
        n += 1
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&'+\
            'symbol='+symbol +'&apikey='+API_KEY
        r = requests.get(url)
        data = r.json()
        if( ("Note" in data) and ("Thank you" in data["Note"])):
            time.sleep(SLEEP_TIME)
            data ={}
        else:
            return data
    return data
    

def company_overview(symbol):
    n = 0
    while (n <MAX_TRIES):
        n += 1
        url = 'https://www.alphavantage.co/query?function=OVERVIEW&'+\
            'symbol='+symbol +'&apikey='+API_KEY
        r = requests.get(url)
        data = r.json()
        if( ("Note" in data) and ("Thank you" in data["Note"])):
            time.sleep(SLEEP_TIME)
            data ={}
        else:
            return data
    return data
    

def earnings(symbol):
    n = 0
    while (n <MAX_TRIES):
        n += 1
        url = 'https://www.alphavantage.co/query?function=EARNINGS&'+\
            'symbol='+symbol +'&apikey='+API_KEY
        r = requests.get(url)
        data = r.json()
        if( ("Note" in data) and ("Thank you" in data["Note"])):
            time.sleep(SLEEP_TIME)
            data ={}
        else:
            return data
    return data
    

def quote(symbol):
    n = 0
    while (n <MAX_TRIES):
        n += 1
        url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&'+\
            'symbol='+symbol +'&apikey='+API_KEY
        r = requests.get(url)
        data = r.json()
        if( ("Note" in data) and ("Thank you" in data["Note"])):
            time.sleep(SLEEP_TIME)
            data ={}
        else:
            return data
    return data
    

def search(keywords):
    n = 0
    while (n <MAX_TRIES):
        n += 1
        url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&'+'keywords='+keywords+'&apikey='+API_KEY
        r = requests.get(url)
        data = r.json()
        if( ("Note" in data) and ("Thank you" in data["Note"])):
            time.sleep(SLEEP_TIME)
            data ={}
        else:
            return data
    return data
