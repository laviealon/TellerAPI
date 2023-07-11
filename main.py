import zlib
from flask import Flask, jsonify, request
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


@app.route('/signin/mfa/<method>', methods=['POST'])
def mfa_verify(method):
    credentials = teller_api.Credentials(
        teller_mission=curr_session.teller_mission,
        user_agent=teller_api.USER_AGENT,
        api_key=teller_api.API_KEY,
        device_id=curr_session.device_id,
        r_token=curr_session.r_token,
        f_token=curr_session.f_token,
    )
    mfa_token = method.lower() + '_' + curr_session.mfa_id
    response = teller_api.request_mfa_method(credentials, mfa_token)
    curr_session.teller_mission = response.headers['teller-mission']
    curr_session.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], curr_session.username,
                                                      response.headers['f-request-id'], curr_session.device_id,
                                                      teller_api.API_KEY)
    curr_session.r_token = response.headers['r-token']
    return response.json()



@app.route('/signin/mfa/verify/<code>/<session_token>', methods=['POST'])
def mfa_verify_code(code, session_token):
    session_token = zlib.decompress(session_token).decode('utf-8').split(':')
    credentials = teller_api.Credentials(
        teller_mission=session_token[0],
        user_agent=teller_api.USER_AGENT,
        api_key=teller_api.API_KEY,
        device_id=session_token[5],
        r_token=session_token[2],
        f_token=teller_api.extract_f_token(session_token[3], session_token[4], session_token[1], session_token[5], teller_api.API_KEY),
    )
    response = teller_api.verify_mfa(credentials, code)
    token_body = response.headers['teller-mission'] + ':' + response.headers['f-request-id'] + ':' + response.headers['r-token'] + ':' + response.headers['f-token-spec'] + ':' + session_token[4] + ':' + session_token[5]
    session_token = zlib.compress(token_body.encode('utf-8'))
    return jsonify({
        'session_token': session_token,
    })



if __name__ == '__main__':
    app.run()