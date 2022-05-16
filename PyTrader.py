from email import header
from time import gmtime, strftime
import pandas
import yfinance as yf;
from pandas_datareader import data as pd
import urllib3
import json

http = urllib3.PoolManager()


f = open("user.json","+r")
Account=json.load(f)
f.close

user = Account['user']
key = Account['key']
authorization = Account['authorization']


def getCurrentAction(enterment : str):
    data = yf.download(enterment, group_by="column",period='1d')
    currentAction = data['Close'].values[0]
    float(currentAction)
    return currentAction

def getOrdersAccount():
    url1= f"https://streaming.saxotrader.com/sim/openapi/streaming/connection?authorization=BEARER{authorization}&contextID=explorer_1652715200460"
    r=http.request('GET',url1)
    print(r.status)
    return r.data
    
print (getCurrentAction("RI.PA"))
print (getOrdersAccount())
