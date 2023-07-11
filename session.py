class Session:
    def __init__(self, **kwargs):
        self.id = id(self)
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.device_id = kwargs.get('device_id')
        self.teller_mission = kwargs.get('teller_mission')
        self.user_agent = kwargs.get('user_agent')
        self.api_key = kwargs.get('api_key')
        self.r_token = kwargs.get('r_token')
        self.f_token = kwargs.get('f_token')
        self.mfa_id = kwargs.get('mfa_id')
