from credentials import Credentials
from flask import Flask, request
import teller_api
from session import Session

app = Flask(__name__)

USER_AGENT = 'Teller Bank iOS 2.0'
API_KEY = 'HowManyGenServersDoesItTakeToCrackTheBank?'

credentials = Credentials()
credentials.user_agent = USER_AGENT
credentials.api_key = API_KEY


@app.route('/signin', methods=['POST'])
def signin():
    credentials.username = request.json.get('username')
    password = request.json.get('password')
    credentials.device_id = request.json.get('device_id')
    response = teller_api.signin(credentials, password)
    credentials.teller_mission = response.headers['teller-mission']
    credentials.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], credentials.username, response.headers['f-request-id'], credentials.device_id, credentials.api_key)
    credentials.r_token = response.headers['r-token']
    credentials.mfa_id = response.json()['data']['devices'][0]['id'][4:]
    return response.json()


@app.route('/signin/mfa', methods=['POST'])
def mfa_verify():
    mfa_token = request.json.get('method') + '_' + credentials.mfa_id
    response = teller_api.request_mfa_method(credentials, mfa_token)
    credentials.teller_mission = response.headers['teller-mission']
    credentials.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], credentials.username,
                                                      response.headers['f-request-id'], credentials.device_id,
                                                      credentials.api_key)
    credentials.r_token = response.headers['r-token']
    return response.json()



@app.route('/signin/mfa/verify', methods=['POST'])
def mfa_verify_code():
    response = teller_api.verify_mfa(credentials, request.json.get('code'))
    credentials.teller_mission = response.headers['teller-mission']
    credentials.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], credentials.username,
                                                        response.headers['f-request-id'], credentials.device_id,
                                                        credentials.api_key)
    credentials.r_token = response.headers['r-token']
    credentials.a_token = response.json()['data']['a_token']
    return response.json()


@app.route('/accounts', methods=['GET'])
def get_accounts():
    response = teller_api.reauthenticate(credentials)
    credentials.teller_mission = response.headers['teller-mission']
    credentials.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], credentials.username,
                                                        response.headers['f-request-id'], credentials.device_id,
                                                        credentials.api_key)
    credentials.r_token = response.headers['r-token']
    credentials.s_token = response.headers['s-token']
    credentials.a_token = response.json()['data']['a_token']
    return response.json()

@app.route('/accounts/<account_id>/transactions', methods=['GET'])
def get_transactions(account_id):
    response = teller_api.get_transactions(credentials, account_id)
    credentials.teller_mission = response.headers['teller-mission']
    credentials.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], credentials.username,
                                                        response.headers['f-request-id'], credentials.device_id,
                                                        credentials.api_key)
    credentials.r_token = response.headers['r-token']
    credentials.s_token = response.headers['s-token']
    return response.json()


@app.route('/accounts/<account_id>/balances', methods=['GET'])
def get_balances(account_id):
    response = teller_api.get_balances(credentials, account_id)
    credentials.teller_mission = response.headers['teller-mission']
    credentials.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], credentials.username,
                                                        response.headers['f-request-id'], credentials.device_id,
                                                        credentials.api_key)
    credentials.r_token = response.headers['r-token']
    credentials.s_token = response.headers['s-token']
    return response.json()


if __name__ == '__main__':
    app.run()