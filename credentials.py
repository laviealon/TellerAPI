class Credentials:
    """A credentials object to hold all the necessary information to make a request to the Teller API.
    Some attributes may be redundant depending on the request being made. Credentials objects only store
    information that must persist between requests. For example, a user's password is not stored in a
    credentials object because it is only needed for the initial request to sign in.

    Attributes:
        teller_mission (str): The teller mission header.
        f_token (str): The f-token header.
        r_token (str): The r-token header.
        s_token (str): The s-token header.
        a_token (str): The a-token header.
        username (str): The user's username.
        device_id (str): The user's device id.
        mfa_id (str): The mfa id of the user, specific to the mfa flow.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        s = ''
        for key, value in self.__dict__.items():
            s += f'{key}: {value}\n'
        return s

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

    def update(self, response=None, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

