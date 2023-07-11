import zlib

from flask import Flask, jsonify, request
import teller_api

app = Flask(__name__)

@app.route('/signin', methods=['POST'])
def signin():
    username = request.json.get('username')
    password = request.json.get('password')
    device_id = request.json.get('device_id')
    response = teller_api.signin(username, password, device_id)
    return response.json()


@app.route('/signin/mfa/<method>/<session_token>', methods=['POST'])
def mfa_verify(method, session_token):
    session_token = zlib.decompress(session_token).decode('utf-8').split(':')
    credentials = teller_api.Credentials(
        teller_mission=session_token[0],
        user_agent=teller_api.USER_AGENT,
        api_key=teller_api.API_KEY,
        device_id=session_token[5],
        r_token=session_token[2],
        f_token=teller_api.extract_f_token(session_token[3], session_token[4], session_token[1], session_token[5], teller_api.API_KEY),
    )
    mfa_token = session_token[6 + int(method)]
    response = teller_api.request_mfa_method(credentials, mfa_token)
    token_body = response.headers['teller-mission'] + ':' + response.headers['f-request-id'] + ':' + response.headers['r-token'] + ':' + response.headers['f-token-spec'] + ':' + session_token[4] + ':' + session_token[5]
    session_token = zlib.compress(token_body.encode('utf-8'))
    return jsonify({
        'session_token': session_token,
    })


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