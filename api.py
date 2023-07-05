import base64
import hashlib
import json
import re

import requests

API_BASE_URL = 'https://test.teller.engineering'
USER_AGENT = 'Teller Bank iOS 2.0'
API_KEY = 'HowManyGenServersDoesItTakeToCrackTheBank?'


'''
======== SIGNIN FLOW ========
(1) POST /signin with credentials
(2) receive f-token-spec, decode with base64, check for how to decode f-token using API key, username, and f-request-id
(3) POST /signin/mfa with selection, f-token, r-token, device id
(4) repeat step 2
'''


def signin(username, password, device_id):
    headers = {
        'user-agent': USER_AGENT,
        'api-key': API_KEY,
        'device-id': device_id,
        'content-type': 'application/json',
        'accept': 'application/json'
    }
    payload = {
        "password": password,
        "username": username
    }
    response = requests.post(API_BASE_URL + '/signin', headers=headers, json=payload)
    return response


def extract_f_token(f_token_spec, username, f_request_id, device_id):
    """
    Preconditions:
        - f-token-spec is decoded
        - f-token-spec contains placeholders for api-key, username, and last-request-id
    """
    values = {
        'api-key': API_KEY,
        'username': username,
        'last-request-id': f_request_id,
        'device-id': device_id
    }
    placeholder_pattern = re.compile(r'(api-key|username|last-request-id|device-id)')
    placeholders = placeholder_pattern.findall(f_token_spec)
    encoded_f_token = f_token_spec
    for placeholder in placeholders:
        encoded_f_token = encoded_f_token.replace(placeholder, values[placeholder], 1)
    hash_value = hashlib.sha256(encoded_f_token.encode()).digest()
    encoded_hash = base64.b64encode(hash_value).decode()

    return encoded_hash


def request_mfa_method(teller_mission, api_key, device_id, r_token, f_token, method_id):
    if teller_mission == 'https://blog.teller.io/2021/06/21/our-mission.html':
        teller_mission_check = 'accepted!'
    else:
        teller_mission_check = 'rejected!'
    headers = {
        'teller-mission': teller_mission_check,
        'user-agent': USER_AGENT,
        'api-key': api_key,
        'device-id': device_id,
        'r-token': r_token,
        'f-token': f_token,
        'accept': 'application/json'
    }
    payload = {
        "method_id": method_id
    }
    response = requests.post(API_BASE_URL + '/signin/mfa', headers=headers, json=json.dumps(payload))
    return response


if __name__ == '__main__':
    device_id = input("Enter your device ID: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    response = signin(username, password, device_id)
    print(response)
    f_token = extract_f_token(response.headers['f-token-spec'], username, response.headers['f-request-id'], device_id)
    print(f_token)
    mfa_type = int(input("Enter your MFA type (SMS - 0 or VOICE - 1): "))
    response_json = response.json()
    response = request_mfa_method(response.headers['teller-mission'], API_KEY, device_id, response.headers['r-token'], f_token, response_json["data"]["devices"][mfa_type]["id"])
    print(response)



