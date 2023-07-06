import base64
import hashlib
from typing import Dict

import requests

API_BASE_URL = 'https://test.teller.engineering'
USER_AGENT = 'Teller Bank iOS 2.0'
API_KEY = 'HowManyGenServersDoesItTakeToCrackTheBank?'
MFA_CODE = '123456'


'''
======== SIGNIN FLOW ========
(1) POST /signin with credentials
(2) receive f-token-spec, decode with base64, check for how to decode f-token using API key, username, and f-request-id
(3) POST /signin/mfa with selection, f-token, r-token, device id
(4) repeat step 2
'''
class Credentials:
    def __init__(self, teller_mission, user_agent, api_key, device_id, r_token, f_token):
        self.teller_mission = teller_mission
        self.user_agent = user_agent
        self.api_key = api_key
        self.device_id = device_id
        self.r_token = r_token
        self.f_token = f_token

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
    print(headers, payload)
    response = requests.post(API_BASE_URL + '/signin', headers=headers, json=payload)
    return response


def find_symbol(f_token_spec):
    """ This implementation assumes '-' will never be used as the splitting symbol, and allows
    for multiple (2+) non-alphanumeric characters to be used as the splitting symbol.
    """
    symbol_start = -1
    symbol_end = -1

    # Iterate over the characters in the specification string
    for i, char in enumerate(f_token_spec):
        if not char.isalnum() and char != '-':
            # If this is the first non-alphanumeric character, set symbol_start
            if symbol_start == -1:
                symbol_start = i
            # Update symbol_end
            symbol_end = i
        else:
            # If we have found a sequence of non-alphanumeric characters, break the loop
            if symbol_start != -1:
                break

    # If we have found a sequence of non-alphanumeric characters, return it as the symbol
    if symbol_start != -1:
        return f_token_spec[symbol_start:symbol_end + 1]
    else:
        if '--' in f_token_spec:
            return '--'
        else:
            raise Exception('invalid f-token-spec')


def extract_f_token(f_token_spec, username, f_request_id, device_id, api_key):
    var_dict = {
        'username': username,
        'last-request-id': f_request_id,
        'device-id': device_id,
        'api-key': api_key
    }

    # Decode f-token-spec with base64
    f_token_spec = base64.b64decode(f_token_spec).decode('utf-8')

    # Remove the encryption method from the f-token-spec
    cleaned_f_token_spec = f_token_spec[15:len(f_token_spec) - 1]

    split_symb = find_symbol(cleaned_f_token_spec)

    spec_parts = cleaned_f_token_spec.split(split_symb)
    print(spec_parts)

    final_string = ''
    for part in spec_parts:
        if part in var_dict:
            final_string += str(var_dict[part])
            if part != spec_parts[-1]:
                final_string += split_symb
        else:
            continue

    # encrypt the final string with sha256 followed by base64
    final_string = base64.b64encode(hashlib.sha256(final_string.encode('utf-8')).digest()).decode('utf-8')

    return final_string[:-1]


def request_mfa_method(credentials, method_id):
    headers = {
        'teller-mission': teller_mission_check(credentials.teller_mission),
        'user-agent': credentials.user_agent,
        'api-key': credentials.api_key,
        'device-id': credentials.device_id,
        'r-token': credentials.r_token,
        'f-token': credentials.f_token,
        'content-type': 'application/json',
        'accept': 'application/json'
    }
    payload = {
        "device_id": method_id
    }
    return requests.post(API_BASE_URL + '/signin/mfa', headers=headers, json=payload)


def teller_mission_check(teller_mission):
    if teller_mission == 'https://blog.teller.io/2021/06/21/our-mission.html':
        teller_mission_check = 'accepted!'
    else:
        teller_mission_check = 'rejected!'
    return teller_mission_check


def verify_mfa(credentials, mfa_code):
    headers = {
        'teller-mission': teller_mission_check(credentials.teller_mission),
        'user-agent': credentials.user_agent,
        'api-key': credentials.api_key,
        'device-id': credentials.device_id,
        'r-token': credentials.r_token,
        'f-token': credentials.f_token,
        'content-type': 'application/json',
        'accept': 'application/json'
    }
    payload = {
        "code": mfa_code
    }
    return requests.post(API_BASE_URL + '/signin/mfa/verify', headers=headers, json=payload)


if __name__ == '__main__':
    device_id = input("Enter your device ID: ")
    username = "black_max"
    password = "iran"
    response = signin(username, password, device_id)
    print(response.headers)
    print(response.json())
    print(base64.b64decode(response.headers['f-token-spec']).decode('utf-8'))
    f_token = extract_f_token(response.headers['f-token-spec'], username, response.headers['f-request-id'], device_id, API_KEY)
    mfa_type = int(input("Enter your MFA type (SMS - 0 or VOICE - 1): "))
    response_json = response.json()
    credentials = Credentials(response.headers['teller-mission'], USER_AGENT, API_KEY, device_id, response.headers['r-token'], f_token)
    response = request_mfa_method(credentials, response_json["data"]["devices"][mfa_type]["id"])
    print(response.headers)
    print(response.json())
    f_token = extract_f_token(response.headers['f-token-spec'], username, response.headers['f-request-id'], device_id, API_KEY)
    mfa_code = input("Enter your MFA code: ")
    credentials = Credentials(response.headers['teller-mission'], USER_AGENT, API_KEY, device_id, response.headers['r-token'], f_token)
    response = verify_mfa(credentials, mfa_code)
    print(response.json())




