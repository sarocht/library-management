import requests


class InvalidURL(Exception):
    pass


class UnknownError(Exception):
    pass


class Requests:

    @staticmethod
    def get(url):
        try:
            s = requests.get(url)
            if s.status_code == 200:
                return s
            elif s.status_code == 404:
                return InvalidURL
            else:
                return UnknownError
        except:
            return UnknownError
