class ParamException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class PredictException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

