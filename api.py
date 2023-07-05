import base64
import hashlib
import json
import re

import requests

api_base_url = 'https://test.teller.engineering'

'''
======== SIGNIN FLOW ========
(1) POST /signin with credentials
(2) receive f-token-spec, decode with base64, check for how to decode f-token using API key, username, and f-request-id
(3) POST /signin/mfa with selection, f-token, r-token, device id
(4) repeat step 2
'''


def signin(username, password, device_id):
    headers = {
        'user-agent': 'Teller Bank iOS 2.0',
        'api-key': 'HowManyGenServersDoesItTakeToCrackTheBank?',
        'device-id': device_id,
        'content-type': 'application/json',
        'accept': 'application/json'
    }
    payload = {
        "password": password,
        "username": username
    }
    response = requests.post(api_base_url + '/signin', headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Signin failed with status code: ' + str(response.status_code))


def extract_f_token(f_token_spec, api_key, username, f_request_id):
    """
    Preconditions:
        - f-token-spec is decoded
        - f-token-spec contains placeholders for api-key, username, and last-request-id
    """
    values = {
        'api-key': api_key,
        'username': username,
        'last-request-id': f_request_id
    }
    placeholder_pattern = re.compile(r'(api-key|username|last-request-id)')
    placeholders = placeholder_pattern.findall(f_token_spec)
    encoded_f_token = f_token_spec
    for placeholder in placeholders:
        encoded_f_token = encoded_f_token.replace(placeholder, values[placeholder], 1)
    hash_value = hashlib.sha256(encoded_f_token.encode()).digest()
    encoded_hash = base64.b64encode(hash_value).decode()

    return encoded_hash

def request_mfa_method()







# account_id = 'acc_dzuriivntsv6ytxmsmvusze4aecvbddhcglw4ha'

# POST /signin
# user-agent: Teller Bank iOS 2.0
# api-key: HowManyGenServersDoesItTakeToCrackTheBank?
# device-id: 2NLM6CALAAZRDKLJ
# content-type: application/json
# accept: application/json
# {
#   "password": "teller",
#   "username": "numbat"
# }

# headers = {
#     'teller-mission': 'accepted!',
#     'user-agent': 'Teller Bank iOS 2.0',
#     'api-key': 'HowManyGenServersDoesItTakeToCrackTheBank?',
#     'device-id': 'WMVCPICTGFY4GJTY',
#     'r-token': 'QTEyOEdDTQ.dsGewPI5sik1VNDNci8d2cHFMuOUvZS8MJ_sbbWA_nmuMYniNnDzpU9CgFE.GRp4A04BG24Dw8sA.711T9v899pWc9-rVW1M0WfZGOqtport6HhSlGyU_bYWo5NPglH-I-DPLT3aLzFtD9P-BpVzKhpLtq3LlykTtfApYOln8qEtSR_zrNpvxEsbj_uNTqtv7PUG5EUyeYZ8WBslsXXBDQ09I3HhWfjWTn_eDWyg8Bgk8-2ekhF-MMZ3fRHrP8gfqWbOsNMdCHX0xNYJm8759idmlqwMCUyzarld7ntuj.qhV7WNxGzFlR_Y3HkvgT-w',
#     'f-token': 'HzAtpYZ6MXBo/enXBc8ToYMhVf414AGc56ei+tXHMg4',
#     's-token': 'rFsMlwEdpwJQynoHGby04WmOVYR+h/0hz4tY61/3H1w',
#     'accept': 'application/json'
# }
#
# signin_headers = {
#     'user-agent': 'Teller Bank iOS 2.0',
#     'api-key': 'HowManyGenServersDoesItTakeToCrackTheBank?',
#     'device-id': '2NLM6CALAAZRDKLJ',
#     'content-type': 'application/json',
#     'accept': 'application/json'
# }
# #
# signin_payload = {
#     "password": "iran",
#     "username": "black_max"
# }

# account_id = "acc_dzuriivntsv6ytxmsmvusze4aecvbddhcglw4ha"
# details_headers = {
#     "teller-mission" : "accepted!",
#     "user-agent": "Teller Bank iOS 2.0",
#     "api-key": "HowManyGenServersDoesItTakeToCrackTheBank?",
#     "device-id": "ZNCNO67L2N4N46DW",
#     "r-token": "QTEyOEdDTQ.SIRO-amlVSTgJN8UnSoyZHAFeRkjqJxFWNJjPaCM1veEqkMXCh2Aquu5gqo.IdtlK3XCE-PViIQE.pXUX06JNrq174qzpQArmnCJodMyFi1O2BV4u5e1kBsSFnhHKPUB9e6iiJROfj6BnsEh8R4O3fn0QGDJ9YxLss0KXC1tRoCya6TixqJ6_fGqJMuHQc76WClUGq7N3CRRB2ND1XmdNYAgZZS5EzOmRhbftTv6gSU6td5JBudGwLk4R44kDIA-rVUk4CaQpsm-NjKWPoNPcR3QgFr0YL6oy.Moqyn8Oybl6XVmVumlfXaQ",
#     "f-token": "fuWlt/+wT6KGvYPIu2Bsiza3LcBD0H6rYjrPpA/gxnw",
#     "content-type": "application/json",
#     "accept": "application/json",
# }
# payload = {
#   "device_id": "sms_ad_pge6c4d5rqgcxwo7wvk5pvbtpayef5hhhxtcweq"
# }

if __name__ == '__main__':
    # response = requests.post(api_base_url + '/signin', headers=signin_headers, data=json.dumps(signin_payload))
    # print(response.status_code)
    # print(response.json())
    # response = requests.post(f'{api_base_url}/signin/mfa', headers=details_headers, data=json.dumps(payload))
    # print(response.status_code)
    # print(response.json())
    print(extract_f_token('last-request-id%username%api-key', 'HowManyGenServersDoesItTakeToCrackTheBank?', 'black_max','req_ka32gwbmj5swmf7yqlgl47efuvr2cwaio7dlxpy'))
    # response = requests.get(f'{api_base_url}/accounts/{account_id}/transactions', headers=headers)
    # print(response.status_code)
    # print(response.json())
    # response = requests.post(api_base_url + '/signin', headers=signin_headers, data=json.dumps(signin_payload))
    # print(response.status_code)
    # print(response.json())
    # print(response.headers)
    # r_token = response.headers['r-token']
    # f_token = response.headers['f-token-spec']
    # response = requests.post(api_base_url + '/signin/mfa', data=json.dumps({"device_id": "pge6c4d5rqgcxwo7wvk5pvbtpayef5hhhxtcweq"}))
    # print(response.status_code)
    # print(response.json())


