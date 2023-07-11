import base64
import zlib

import requests

url = "http://127.0.0.1:5000"

# headers = {
#     user-agent: Teller Bank iOS 2.0
#     api-key: HowManyGenServersDoesItTakeToCrackTheBank?
#     device-id: XQGZYZXS7KNW7GZ7
#     content-type: application/json
#     accept: application/json
# }

headers = {
    'device-id': 'YDC4EKPFACKHDHG2',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

payload = {
    'username': 'black_max',
    'password': 'iran'
}


if __name__ == '__main__':
    response = requests.request("POST", url + '/signin', headers=headers, json=payload)
    print(response.json())
    # response = requests.request("POST", url + '/signin/mfa/sms')
    # print(response.text)
