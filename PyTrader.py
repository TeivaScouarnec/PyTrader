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

def getIdentifierInstrument(company : str, AssetType : str):
    url = f"https://gateway.saxobank.com/sim/openapi/ref/v1/instruments?KeyWords={company}&AssetTypes={AssetType}"
    r=http.request('GET',url, headers=headerRequest)
    data = json.loads(r.data)
    identifier = data['Data'][0]['Identifier']
    return (int(identifier))

def getUicInstrument(Identifier:int,AssetType : str):
    url = f"https://gateway.saxobank.com/sim/openapi/ref/v1/instruments/details/{Identifier}/{AssetType}"
    r=http.request('GET',url, headers=headerRequest)
    data = json.loads(r.data)
    uic = data['Uic']
    return (int(uic))

def getCurrentAction(Company : str, AssetType : str):
    company = Company
    assetType = AssetType
    identifier = getIdentifierInstrument(company,assetType)
    uic = getUicInstrument(identifier,assetType)
    
    url = f"https://gateway.saxobank.com/sim/openapi/trade/v1/infoprices/list?AccountKey={key}&Uics={uic}&AssetType={AssetType}"
    r=http.request('GET',url, headers=headerRequest)
    data = json.loads(r.data)
    
    currentAction = data['Data'][0]['Quote']['Ask']
    return (float(currentAction))

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
    
print (getCurrentAction(Company="RI:xpar",AssetType="Stock"))
