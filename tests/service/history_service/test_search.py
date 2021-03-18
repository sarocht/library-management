from app.service.history_service import search
from app.helper import common_response

from unittest import mock


@mock.patch("app.model.history.History.search_history_by_isbn")
def test_get_book_by_isbn_success(mock_books):
    history = [
        {
            "action": "Borrowed",
            "action_by": "note",
            "created_by": "nat",
            "isbn": "isbn:1501124021",
            "transaction_date": "2021-03-18 15:35:25",
            "transaction_id": "9d59090b-640f-4c73-aa8a-00227141a9fd"
        },
        {
            "action": "Available",
            "action_by": "note",
            "created_by": "nat",
            "isbn": "isbn:1501124021",
            "transaction_date": "2021-03-18 15:35:27",
            "transaction_id": "e0707ae7-b042-4d23-adec-1cf8fa6edf92"
        },
    ]
    mock_books.return_value = history
    assert search(typ="isbn", isbn="isbn:1234") == {'history': history}
