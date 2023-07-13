import json

import requests
from flask import jsonify

if __name__ == '__main__':
    device_id = "KEP5CM64YHKIXL4F"
    username = "black_max"
    password = "iran"
    req = {
        "username": username,
        "password": password,
        "device_id": device_id
    }
    response = requests.post('http://127.0.0.1:5000/signin', json=req)
    print(response.text)
    req = {
        "method": "sms"
    }
    response = requests.post('http://127.0.0.1:5000/signin/mfa', json=req)
    print(response.text)
    req = {
        "code": "123456"
    }
    response = requests.post('http://127.0.0.1:5000/signin/mfa/verify', json=req)
    print(response.text)
    response = requests.get('http://127.0.0.1:5000/accounts')
    print(response.text)
    response = requests.get('http://127.0.0.1:5000/accounts/acc_oal57fitxo2cl6lgicllypdjxm5jowzokb3cxgq/transactions')
    print(response.text)
    response = requests.get('http://127.0.0.1:5000/accounts')
    print(response.text)
    response = requests.get('http://127.0.0.1:5000/accounts/acc_oal57fitxo2cl6lgicllypdjxm5jowzokb3cxgq/balances')
    print(response.text)
    response = requests.get('http://127.0.0.1:5000/accounts/acc_oal57fitxo2cl6lgicllypdjxm5jowzokb3cxgq/details')
    print(response.text)
