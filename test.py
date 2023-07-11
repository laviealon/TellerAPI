import json

import requests
from flask import jsonify

if __name__ == '__main__':
    device_id = input("Enter your device ID: ")
    username = "black_max"
    password = "iran"
    req = {
        "username": username,
        "password": password,
        "device_id": device_id
    }
    response = requests.post('http://127.0.0.1:5000/signin', json=req)
    print(response.text)
    response = requests.post('http://127.0.0.1:5000/signin/mfa/sms')
