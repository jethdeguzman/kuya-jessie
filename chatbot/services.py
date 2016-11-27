import json
import requests
import uuid

UNIONBANK_URL = 'https://api.us.apiconnect.ibmcloud.com/ubpapi-dev/sb/api/RESTs/{method}' 
UNIONBANK_HEADERS = {
    'x-ibm-client-id' : '548e3521-aaad-426f-a5db-539b3a39a02a',
    'x-ibm-client-secret' : 'N1sH7xD6oX2tD7iJ5nP5uY7xG6eO0xQ5dD5gC8wD3uC4lF1aH8',
    'content-type': 'application/json',
    'accept': 'application/json'
}

USER_TYPE_ACCOUNT_MAP = {
    'CUSTOMER' : '100789269141',
    'AGENT' : '101754145386',
    'APP' : '102100162636'
}

def get_account_info(type):
    try:
        url = UNIONBANK_URL.format(method='getAccount') + '?account_no=' + USER_TYPE_ACCOUNT_MAP[type]
        response = requests.get(url, headers=UNIONBANK_HEADERS)
        result =  response.json()[0]
    except Exception:
        return {'current_balance' : '0.00'}

    return result

def transfer_funds(source_account_type, target_account_type, amount=0.00):
    try:
        url = UNIONBANK_URL.format(method='transfer')
        data = {
            'channel_id' : 'BLUEMIX',
            'transaction_id' : str(uuid.uuid4()),
            'source_account' : USER_TYPE_ACCOUNT_MAP[source_account_type],
            'source_currency' : 'php',
            'target_account' : USER_TYPE_ACCOUNT_MAP[target_account_type],
            'target_currency' : 'php',
            'amount' : amount
        }
        print data
        response = requests.post(url, headers=UNIONBANK_HEADERS, json=data)
        print response
    except Exception:
        pass

    return 

