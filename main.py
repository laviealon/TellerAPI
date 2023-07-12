from credentials import Credentials
from flask import Flask, request
import teller_api as teller

app = Flask(__name__)
credentials = Credentials()


@app.route('/signin', methods=['POST'])
def signin():
    credentials.update(
        username=request.json.get('username'),
        device_id=request.json.get('device_id')
    )
    password = request.json.get('password')
    response = teller.signin(credentials, password)
    credentials.update(
        teller_mission=response.headers['teller-mission'],
        f_token=teller.extract_f_token(response.headers['f-token-spec'], credentials.username,
                                       response.headers['f-request-id'], credentials.device_id, teller.API_KEY),
        r_token=response.headers['r-token'],
        mfa_id=response.json()['data']['devices'][0]['id'][4:]
    )
    return response.json()


@app.route('/signin/mfa', methods=['POST'])
def mfa_verify():
    mfa_token = request.json.get('method') + '_' + credentials.mfa_id
    response = teller.request_mfa_method(credentials, mfa_token)
    credentials.update(
        teller_mission=response.headers['teller-mission'],
        f_token=teller.extract_f_token(response.headers['f-token-spec'], credentials.username,
                                                 response.headers['f-request-id'], credentials.device_id,
                                                 teller.API_KEY),
        r_token=response.headers['r-token']
    )
    return response.json()


@app.route('/signin/mfa/verify', methods=['POST'])
def mfa_verify_code():
    response = teller.verify_mfa(credentials, request.json.get('code'))
    credentials.update(
        teller_mission=response.headers['teller-mission'],
        f_token=teller.extract_f_token(response.headers['f-token-spec'], credentials.username,
                                                 response.headers['f-request-id'], credentials.device_id,
                                                 teller.API_KEY),
        r_token=response.headers['r-token'],
        s_token=response.headers['s-token'],
        a_token=response.json()['data']['a_token']
    )
    return {'status': 'success'}


@app.route('/accounts', methods=['GET'])
def get_accounts():
    response = teller.reauthenticate(credentials)
    credentials.update(
        teller_mission=response.headers['teller-mission'],
        f_token=teller.extract_f_token(response.headers['f-token-spec'], credentials.username,
                                       response.headers['f-request-id'], credentials.device_id,
                                       teller.API_KEY),
        r_token=response.headers['r-token'],
        s_token=response.headers['s-token'],
        a_token=response.json()['data']['a_token']
    )
    return response.json()


@app.route('/accounts/<account_id>/transactions', methods=['GET'])
def get_transactions(account_id):
    response = teller.get_transactions(credentials, account_id)
    credentials.update(
        teller_mission=response.headers['teller-mission'],
        f_token=teller.extract_f_token(response.headers['f-token-spec'], credentials.username,
                                       response.headers['f-request-id'], credentials.device_id,
                                       teller.API_KEY),
        r_token=response.headers['r-token'],
        s_token=response.headers['s-token']
    )
    return response.json()


@app.route('/accounts/<account_id>/balances', methods=['GET'])
def get_balances(account_id):
    response = teller.get_balances(credentials, account_id)
    credentials.update(
        teller_mission=response.headers['teller-mission'],
        f_token=teller.extract_f_token(response.headers['f-token-spec'], credentials.username,
                                       response.headers['f-request-id'], credentials.device_id,
                                       teller.API_KEY),
        r_token=response.headers['r-token'],
        s_token=response.headers['s-token']
    )
    return response.json()


if __name__ == '__main__':
    app.run()
