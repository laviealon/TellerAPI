class Session:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        s = ''
        for key, value in self.__dict__.items():
            s += f'{key}: {value}\n'
        return s