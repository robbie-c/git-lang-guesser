import requests

class RequestFailed(Exception):
    def __init__(self, response: requests.Response):
        super(RequestFailed, self).__init__()
        self.response = response