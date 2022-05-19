from multiprocessing.dummy import Array
from typing import List
import urllib3
import json


http = urllib3.PoolManager()

def _createUserFile():
    f = open("user.json", "w+")
    data = {
        "key":"",
        "authorization":""
    }
    json.dump(data,f)
    f.close()

# Verify if a file user.json exist
try:
    f = open("user.json","+r")
except OSError:
    _createUserFile()
    input("Veuillez remplir le fichier 'user.json' avec vos identifiants! -appuyez sur Entrée pour sortir du programme-")
    exit()
else:
    Account=json.load(f)
    f.close


key = Account['key']
authorization = Account['authorization']
headerRequest = {
    "Authorization": f"Bearer {authorization}",
    'Content-Type': 'application/json'
}

                                            #-----------#
                                            #--- API ---#
                                            #-----------#


def getIdentifierInstrument(company : str, AssetType : str):
    """
    Retrieves a company ID by its symbol on SaxoBank to get the UIC instrument.

    Args:
        company (str): The symbol that designates the company (example: for Netflix "NFLX:xnas").
        AssetType (str): AssetType of instrument traded.

    Returns:
        int : Return company ID.
    """
    url = f"https://gateway.saxobank.com/sim/openapi/ref/v1/instruments?KeyWords={company}&AssetTypes={AssetType}"
    r=http.request('GET',url, headers=headerRequest)
    data = json.loads(r.data)
    identifier = data['Data'][0]['Identifier']
    return (int(identifier))


def getUicInstrument(Identifier:int,AssetType : str):
    """
    Retrieves a company UIC with his identifier Instrument.

    Args:
        Identifier (int): company ID
        AssetType (str): AssetType of instrument traded.

    Returns:
        int : Return company Identifier.
    """
    url = f"https://gateway.saxobank.com/sim/openapi/ref/v1/instruments/details/{Identifier}/{AssetType}"
    r=http.request('GET',url, headers=headerRequest)
    data = json.loads(r.data)
    uic = data['Uic']
    return (int(uic))

def getCurrentAction(Company : str, AssetType : str):
    """
    Gets the current stock exchange of a company thanks to its symbol linked to Saxobank and its types of goods.

    Args:
        Company (str): symbol of company
        AssetType (str): AssetType of instrument traded.

    Returns:
        float : Return the current stock exchange of the company.
    """
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
    """
    Gets all the actions performed on the account.
    
    Returns:
        JSON : return data in json.
    """
    urlSaxo= f"https://gateway.saxobank.com/sim/openapi/cs/v1/audit/orderactivities/?AccountKey={key}"
    r=http.request('GET',urlSaxo, headers=headerRequest)
    if (r.status == 200):
        return (json.loads(r.data))
    else:
        return (str("null"))

def getOrderAccount(orderID:int):
    """
    Get a action with his orderID performed on the account.

    Args:
        orderID (int) : Order Identifier

    Returns:
        JSON : return data in json.
    """
    urlSaxo= f"https://gateway.saxobank.com/sim/openapi/cs/v1/audit/orderactivities/?AccountKey={key}&OrderId={orderID}"
    r=http.request('GET',urlSaxo, headers=headerRequest)
    if (r.status == 200):
        return (json.loads(r.data))
    else:
        return (str("null"))

def cancelOrderAccount(OrderIds:List=[]):
    """
    Cancels one or more orders placed.

    Args:
        OrderIds (list):  A list of orders. Default to [].

    Returns:
        JSON : return data in json.
    """
    urlSaxo= f"https://gateway.saxobank.com/sim/openapi/trade/v2/orders/{OrderIds}/?AccountKey={key}"
    r=http.request('DELETE',urlSaxo, headers= headerRequest)
    return (json.loads(r.data))

def cancelAllOrdersAccount(Company:str,AssetType:str="Stock"):
    """
    Cancels all orders placed related to a company.

    Args:
        Company (str): symbol of company
        AssetType (str, optional): AssetType of instrument traded. Defaults to "Stock".

    Returns:
        JSON : return data in json.
    """
    identifier=getIdentifierInstrument(Company,AssetType)
    UIC=getUicInstrument(identifier,AssetType)

    urlSaxo= f"https://gateway.saxobank.com/sim/openapi/trade/v2/orders/?AccountKey={key}&AssetType={AssetType}&Uic={UIC}"
    r=http.request('DELETE',urlSaxo, headers= headerRequest)
    return (json.loads(r.data))


def buyOrder(Company:str,AssetType:str="Stock",Amount:float=0.0):
    """
    Buy a order to a company.

    Args:
        Company (str): symbol of company
        AssetType (str, optional): AssetType of instrument traded. Defaults to "Stock".
        Amount (float, optional): amount of order. Defaults to 0.0.

    Returns:
        JSON: return l'order identify
    """

    identifier = getIdentifierInstrument(company=Company, AssetType=AssetType)
    uic = getUicInstrument(identifier,AssetType=AssetType)
    
    urlSaxo= f"https://gateway.saxobank.com/sim/openapi/trade/v2/orders"
    datarOrder = json.dumps({
        "Uic": uic,
        "AssetType": AssetType,
        "Amount": Amount,
        "BuySell": "Buy",
        "OrderType": "Market",
        "AmountType": "Quantity",
        "ManualOrder": False,
        "OrderDuration": {
            "DurationType": "DayOrder"
        }
    })
    r=http.request('POST',urlSaxo, headers= headerRequest, body= datarOrder)
    return (json.loads(r.data))

def sellOrder(Company:str,AssetType:str="Stock",Amount:float=0.0):
    """
    sell a order to a company.

    Args:
        Company (str): symbol of company
        AssetType (str, optional): AssetType of instrument traded. Defaults to "Stock".
        Amount (float, optional): amount of order. Defaults to 0.0.

    Returns:
        JSON: return l'order identify
    """
    identifier = getIdentifierInstrument(company=Company, AssetType=AssetType)
    uic = getUicInstrument(identifier,AssetType=AssetType)
    
    urlSaxo= f"https://gateway.saxobank.com/sim/openapi/trade/v2/orders"
    datarOrder = json.dumps({
        "Uic": uic,
        "AssetType": AssetType,
        "Amount": Amount,
        "BuySell": "Sell",
        "OrderType": "Market",
        "AmountType": "Quantity",
        "ManualOrder": False,
        "OrderDuration": {
            "DurationType": "DayOrder"
        }
    })
    r=http.request('POST',urlSaxo, headers= headerRequest, body= datarOrder)
    return (json.loads(r.data))
