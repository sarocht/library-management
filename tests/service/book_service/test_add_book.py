from app.service.books_service import add_book
from app.helper import common_response

from unittest import mock


@mock.patch("app.model.books.Books.add_book")
@mock.patch("app.external_api.google_books.GoogleBookAPI.search_books")
@mock.patch("app.model.books.Books.get_book_by_isbn")
def test_add_book_success(mock_books, mock_search_books, mock_add_book):
    mock_books.return_value = []
    mock_search_books.return_value = {
        "totalItems": 1,
        "items": [
            {
                "volumeInfo": {
                    "title": "Principles",
                    "subtitle": "Life and Work",
                    "publisher": "Simon and Schuster",
                    "publishedDate": "2017-09-19",
                    "industryIdentifiers": [
                        {
                            "type": "ISBN_13",
                            "identifier": "9781501124020"
                        },
                        {
                            "type": "ISBN_10",
                            "identifier": "1501124021"
                        }
                    ],
                    "pageCount": 592,
                    "infoLink": "http://books.google.co.th/books?id=okk1DwAAQBAJ&dq=isbn:1501124021&hl=&source=gbs_api",
                }
            }
        ]
    }
    mock_add_book.return_value = None
    rsp = add_book(isbn="isbn:1234")
    assert rsp == common_response.SUCCESS


@mock.patch("app.model.books.Books.get_book_by_isbn")
def test_add_book_failed_database_error(mock_books):
    mock_books.side_effect = KeyError('database error')
    rsp, rsp_status = add_book(isbn="isbn:1234")
    assert rsp == common_response.DATABASE_ERROR[0]
    assert rsp_status == common_response.DATABASE_ERROR[1]


@mock.patch("app.model.books.Books.get_book_by_isbn")
def test_add_book_failed_book_already_exists(mock_books):
    mock_books.return_value = [{'isbn': 'isbn:1234', 'title': 'Principles'}]
    assert add_book(isbn="isbn:1234") == {
        "status": "failed",
        "error_message": "book already exists"
    }


@mock.patch("app.external_api.google_books.GoogleBookAPI.search_books")
@mock.patch("app.model.books.Books.get_book_by_isbn")
def test_add_book_failed_book_cannot_make_a_request_to_google_api(mock_books, mock_search_books):
    mock_books.return_value = []
    mock_search_books.side_effect = KeyError('request error')
    rsp, rsp_status = add_book(isbn="isbn:1234")
    assert rsp == {
        "status": "failed",
        "error_message": "cannot make a request"
    }
    assert rsp_status == 500
