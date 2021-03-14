from app.helper.custom_requests import Requests as Req, InvalidURL, UnknownError


class GoogleBookAPI:

    @staticmethod
    def search_books(query: str):
        try:
            req = Req.get(url=f"https://www.googleapis.com/books/v1/volumes?q={query}")
            return req.json()
        except Exception as e:
            return e
