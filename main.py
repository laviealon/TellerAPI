import zlib
from redis import Redis
from flask import Flask, jsonify, request, Response, session
import teller_api
from session import Session

app = Flask(__name__)

my_session = Session()


@app.route('/signin', methods=['POST'])
def signin():
    my_session.username = request.form['username']
    my_session.password = request.form['password']
    my_session.device_id = request.form['device_id']
    response = teller_api.signin(my_session.username, my_session.password, my_session.device_id)
    my_session.teller_mission = response.headers['teller-mission']
    my_session.user_agent = response.headers['user-agent']
    my_session.api_key = response.headers['api-key']
    my_session.r_token = response.headers['r-token']
    my_session.f_token = teller_api.extract_f_token(response.headers['f-token-spec'], my_session.username, response.headers['f-request-id'], my_session.device_id, my_session.api_key)
    my_session.mfa_id = response['data']['devices'][0]['id'][4:]
    return jsonify({"session_id": my_session.id})


@app.route('/<id>/signin/mfa/<method>', methods=['POST'])
def mfa_verify(method):
    if id != session['id']:
        return jsonify({
            'error': 'invalid session'
        })
    credentials = teller_api.Credentials(
        teller_mission=my_session.teller_mission,
        user_agent=my_session.user_agent,
        api_key=my_session.api_key,
        device_id=my_session.device_id,
        r_token=my_session.r_token,
        f_token=my_session.f_token
    )
    response = teller_api.request_mfa_method(credentials, method.lower() + '_' + my_session.mfa_id)
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
    token_body = response.headers['teller-mission'] + ':' + session_token[5] + ':' + response.json()['data']['a_token']
    session_token = zlib.compress(token_body.encode('utf-8'))
    return jsonify({
        'session_token': session_token,
    })

@app.route('/accounts/<session_token>', methods=['GET'])
def accounts(session_token):
    session_token = zlib.decompress(session_token).decode('utf-8').split(':')
    credentials = teller_api.Credentials(
        teller_mission=session_token[0],
        user_agent=teller_api.USER_AGENT,
        api_key=teller_api.API_KEY,
        device_id=session_token[5],
    )
    a_token = session_token[2]
    response = teller_api.reauthenticate(credentials, a_token)
    return response.json()


# @app.route('/accounts/<account_id>/details')
#
# @app.route('/accounts/<account_id>/transactions')
#
# @app.route('/accounts/<account_id>/balances')
#
# @app.route('/reauth')


if __name__ == '__main__':
    app.run(debug=True)