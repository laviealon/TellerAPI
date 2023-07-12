from credentials import Credentials
from flask import Flask, request
import teller_api
from session import Session

app = Flask(__name__)

curr_session = Session()


@app.route('/signin', methods=['POST'])
def signin():
    curr_session.username = request.json.get('username')
    curr_session.password = request.json.get('password')
    curr_session.device_id = request.json.get('device_id')
    response = teller_api.signin(curr_session.username, curr_session.password, curr_session.device_id)
    curr_session.teller_mission = response.headers['teller-mission']
    curr_session.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], curr_session.username, response.headers['f-request-id'], curr_session.device_id, teller_api.API_KEY)
    curr_session.r_token = response.headers['r-token']
    curr_session.mfa_id = response.json()['data']['devices'][0]['id'][4:]
    return response.json()


@app.route('/signin/mfa', methods=['POST'])
def mfa_verify():
    credentials = Credentials(
        teller_mission=curr_session.teller_mission,
        user_agent=teller_api.USER_AGENT,
        api_key=teller_api.API_KEY,
        device_id=curr_session.device_id,
        r_token=curr_session.r_token,
        f_token=curr_session.f_token
    )
    mfa_token = request.json.get('method') + '_' + curr_session.mfa_id
    print(mfa_token)
    response = teller_api.request_mfa_method(credentials, mfa_token)
    curr_session.teller_mission = response.headers['teller-mission']
    curr_session.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], curr_session.username,
                                                      response.headers['f-request-id'], curr_session.device_id,
                                                      teller_api.API_KEY)
    curr_session.r_token = response.headers['r-token']
    return response.json()



@app.route('/signin/mfa/verify', methods=['POST'])
def mfa_verify_code():
    credentials = Credentials(
        teller_mission=curr_session.teller_mission,
        user_agent=teller_api.USER_AGENT,
        api_key=teller_api.API_KEY,
        device_id=curr_session.device_id,
        r_token=curr_session.r_token,
        f_token=curr_session.f_token
    )
    response = teller_api.verify_mfa(credentials, request.json.get('code'))
    curr_session.teller_mission = response.headers['teller-mission']
    curr_session.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], curr_session.username,
                                                        response.headers['f-request-id'], curr_session.device_id,
                                                        teller_api.API_KEY)
    curr_session.r_token = response.headers['r-token']
    curr_session.a_token = response.json()['data']['a_token']
    return response.json()


@app.route('/accounts', methods=['GET'])
def get_accounts():
    credentials = Credentials(
        user_agent=teller_api.USER_AGENT,
        api_key=teller_api.API_KEY,
        device_id=curr_session.device_id,
    )
    response = teller_api.reauthenticate(credentials, curr_session.a_token)
    curr_session.teller_mission = response.headers['teller-mission']
    curr_session.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], curr_session.username,
                                                        response.headers['f-request-id'], curr_session.device_id,
                                                        teller_api.API_KEY)
    curr_session.r_token = response.headers['r-token']
    curr_session.s_token = response.headers['s-token']
    curr_session.a_token = response.json()['data']['a_token']
    return response.json()

@app.route('/accounts/<account_id>/transactions', methods=['GET'])
def get_transactions(account_id):
    credentials = Credentials(
        teller_mission=curr_session.teller_mission,
        user_agent=teller_api.USER_AGENT,
        api_key=teller_api.API_KEY,
        device_id=curr_session.device_id,
        r_token=curr_session.r_token,
        f_token=curr_session.f_token
    )
    response = teller_api.get_transactions(credentials, curr_session.s_token, account_id)
    curr_session.teller_mission = response.headers['teller-mission']
    curr_session.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], curr_session.username,
                                                        response.headers['f-request-id'], curr_session.device_id,
                                                        teller_api.API_KEY)
    curr_session.r_token = response.headers['r-token']
    curr_session.s_token = response.headers['s-token']
    return response.json()


@app.route('/accounts/<account_id>/balances', methods=['GET'])
def get_balances(account_id):
    credentials = Credentials(
        teller_mission=curr_session.teller_mission,
        user_agent=teller_api.USER_AGENT,
        api_key=teller_api.API_KEY,
        device_id=curr_session.device_id,
        r_token=curr_session.r_token,
        f_token=curr_session.f_token
    )
    response = teller_api.get_balances(credentials, curr_session.s_token, account_id)
    curr_session.teller_mission = response.headers['teller-mission']
    curr_session.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], curr_session.username,
                                                        response.headers['f-request-id'], curr_session.device_id,
                                                        teller_api.API_KEY)
    curr_session.r_token = response.headers['r-token']
    curr_session.s_token = response.headers['s-token']
    return response.json()


if __name__ == '__main__':
    app.run()