class Credentials:
    """A credentials object to hold all the necessary information to make a request to the Teller API.
    Some attributes may be redundant depending on the request being made. Credentials objects are only
    used after the initial sign-in request.

    Attributes necessary for reauthentication (main.get_accounts):
        - user_agent (str): The user-agent header from the previous request.
        - api_key (str): The API key from the previous request.
        - device_id (str): The device ID from the previous request.
    Attributes necessary for all other requests:
        - teller_mission (str): The teller-mission header from the previous request.
        - user_agent (str): The user-agent header from the previous request.
        - api_key (str): The API key from the previous request.
        - device_id (str): The device ID from the previous request.
        - r_token (str): The r-token header from the previous request.
        - f_token (str): The f-token header from the previous request.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        s = ''
        for key, value in self.__dict__.items():
            s += f'{key}: {value}\n'
        return s