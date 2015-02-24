
class RequestFailed(Exception):
    def __init__(self, response):
        super(RequestFailed, self).__init__()
        self.response = response