# Teller API Integration

A simple application providing access to the Teller API implemented in Python 3 
using the [Flask](https://flask.palletsprojects.com/en/1.1.x/) framework.

## Usage

After forking the repository and installing dependencies, the application ```main.py``` can be run.

The application will be available at http://localhost:5000, and this is the endpoint to which API calls should be made.
Running the application instantiates a ```Credentials``` object for the session.

### Endpoints

The application provides the following endpoints:
 - ```/signin``` (POST) - signs in to the Teller API, returning JSON-formatted information for MFA selection. Example usage:
```
 req = {
        "username": username,
        "password": password,
        "device_id": device_id
    }
    response = requests.post('http://127.0.0.1:5000/signin', json=req)
 ```
 - ```/siginin/mfa``` (POST) - selects an MFA method. The choices are ```sms``` or ```voice```. Example usage:
```
req = {
        "method": "sms"
    }
    response = requests.post('http://127.0.0.1:5000/signin/mfa', json=req)
```
 - ```/signin/mfa/verify``` (POST) - submits the MFA code. Example usage: 
```
req = {
        "code": "123456"
    }
    response = requests.post('http://127.0.0.1:5000/signin/mfa/verify', json=req)
```
 - ```/accounts``` (GET) - lists all accounts for the user signed in to the session. Also serves as re-authentication for the session, so hit this endpoint if the session times out.
 - ```/accounts/<account_id>/transactions``` (GET) - lists all transactions for the given account_id, provided by the user and found in JSON responses from previous API calls.
 - ```/accounts/<account_id>/balances``` (GET) - lists all balances for the given account_id, provided by the user and found in JSON responses from previous API calls.

### Signin Flow

The signin flow **must** be followed in order (```signin → mfa → verify → accounts```). Once the user has signed in, the session is authenticated, and they can access account information. After the session times out, they must hit the ```accounts``` endpoint.

## Design

There are a few features of the application that are worth noting:
 - The ```Credentials``` class essentially acts as a session object, storing information about the user necessary for subsequent API calls, in order that the user does not have to make a complex request.
 - The ```teller_api``` module is a wrapper for the API calls, and is responsible for making the requests to the Teller API. It is also responsible for parsing the responses and returning the API responses to the user.






