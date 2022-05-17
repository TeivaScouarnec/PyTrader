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
headerRequest = {
    "Authorization": f"Bearer {authorization}",
    'Content-Type': 'application/json'
}

def getCurrentAction(company : str):
    data = yf.download(company, group_by="column",period='1d')
    currentAction = data['Close'].values[0]
    float(currentAction)
    return currentAction

def getAllOrdersAccount():
    urlSaxo= f"https://gateway.saxobank.com/sim/openapi/port/v1/orders/me"
    r=http.request('GET',urlSaxo, headers=headerRequest)
    if (r.status == 200):
        return (json.loads(r.data))
    else:
        return (str("null"))

def sellOrder():
    urlSaxo= f"https://gateway.saxobank.com/sim/openapi/trade/v2/orders"
    datarOrder = json.dumps({
        "Uic": 21,
        "AssetType": "FxSpot",
        "Amount": 10000,
        "BuySell": "Buy",
        "OrderType": "Market",
        "AmountType": "Quantity",
        "ManualOrder": False,
        "OrderDuration": {
            "DurationType": "DayOrder"
        }
    })
    r=http.request('POST',urlSaxo, headers= headerRequest, body= datarOrder)
    print (r.status)
    return r.data
    
print (getCurrentAction("RI.PA"))
print (getAllOrdersAccount())
