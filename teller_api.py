import base64
import hashlib
import requests
from flask import Flask
from Crypto.Cipher import AES

app = Flask(__name__)

API_BASE_URL = 'https://test.teller.engineering'
USER_AGENT = 'Teller Bank iOS 2.0'
API_KEY = 'HowManyGenServersDoesItTakeToCrackTheBank?'


def signin(credentials, password):
    headers = {
        'user-agent': USER_AGENT,
        'api-key': API_KEY,
        'device-id': credentials.device_id,
        'content-type': 'application/json',
        'accept': 'application/json'
    }
    payload = {
        "password": password,
        "username": credentials.username
    }
    response = requests.post(API_BASE_URL + '/signin', headers=headers, json=payload)
    return response


def request_mfa_method(credentials, method_id):
    headers = {
        'teller-mission': _teller_mission_check(credentials.teller_mission),
        'user-agent': USER_AGENT,
        'api-key': API_KEY,
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


def verify_mfa(credentials, mfa_code):
    headers = {
        'teller-mission': _teller_mission_check(credentials.teller_mission),
        'user-agent': USER_AGENT,
        'api-key': API_KEY,
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


def get_transactions(credentials, account_id):
    headers = {
        'teller-mission': _teller_mission_check(credentials.teller_mission),
        'user-agent': USER_AGENT,
        'api-key': API_KEY,
        'device-id': credentials.device_id,
        'r-token': credentials.r_token,
        'f-token': credentials.f_token,
        's-token': credentials.s_token,
        'accept': 'application/json'
    }
    return requests.get(API_BASE_URL + '/accounts/' + account_id + '/transactions', headers=headers)


def get_balances(credentials, account_id):
    headers = {
        'teller-mission': _teller_mission_check(credentials.teller_mission),
        'user-agent': USER_AGENT,
        'api-key': API_KEY,
        'device-id': credentials.device_id,
        'r-token': credentials.r_token,
        'f-token': credentials.f_token,
        's-token': credentials.s_token,
        'accept': 'application/json'
    }
    return requests.get(API_BASE_URL + '/accounts/' + account_id + '/balances', headers=headers)


def get_details(credentials, account_id):
    headers = {
        'teller-mission': _teller_mission_check(credentials.teller_mission),
        'user-agent': USER_AGENT,
        'api-key': API_KEY,
        'device-id': credentials.device_id,
        'r-token': credentials.r_token,
        'f-token': credentials.f_token,
        's-token': credentials.s_token,
        'accept': 'application/json'
    }
    return requests.get(API_BASE_URL + '/accounts/' + account_id + '/details', headers=headers)


def reauthenticate(credentials):
    headers = {
        'user-agent': USER_AGENT,
        'api-key': API_KEY,
        'device-id': credentials.device_id,
        'content-type': 'application/json',
        'accept': 'application/json'
    }
    payload = {
        "token": credentials.a_token
    }
    return requests.post(API_BASE_URL + '/signin/token', headers=headers, json=payload)


def _teller_mission_check(teller_mission):
    if teller_mission == 'https://blog.teller.io/2021/06/21/our-mission.html':
        teller_mission_check = 'accepted!'
    else:
        teller_mission_check = 'rejected!'
    return teller_mission_check


def _find_symbol(f_token_spec):
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

    split_symb = _find_symbol(cleaned_f_token_spec)

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


def decrypt_account_number(cipher_data, enc_key):
    key = base64.b64decode(eval(base64.b64decode(enc_key))['key'])
    ct, nonce, t = map(base64.b64decode, cipher_data.split(_find_symbol(cipher_data)))
    cipher_data = AES.new(key, AES.MODE_GCM, nonce)
    return cipher_data.decrypt(ct).decode()


