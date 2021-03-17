from app.service.books_service import get_book
from app.helper import common_response

from unittest import mock


@mock.patch("app.model.books.Books.get_book_by_isbn")
def test_get_book_by_isbn_success(mock_books):
    books = [{'isbn': 'isbn:1234', 'title': 'Principles'}]
    mock_books.return_value = books
    assert get_book(typ="isbn", isbn="isbn:1234") == {'books': books}


@mock.patch("app.model.books.Books.get_book_by_title")
def test_get_book_by_book_title_success(mock_books):
    books = [{'isbn': 'isbn:1234', 'title': 'Principles'}]
    mock_books.return_value = books
    assert get_book(typ="title", isbn="Principles") == {'books': books}


def test_get_book_failed_invalid_type():
    books = get_book(typ="invalidtype")
    rsp = books[0]
    rsp_code = books[1]
    assert rsp == {
        "status": "failed",
        "error_message": "invalid typ"
    }
    assert rsp_code == 400


@mock.patch("app.model.books.Books.get_book_by_isbn")
def test_get_book_failed_database_error(mock_books):
    mock_books.side_effect = KeyError('database error')
    books = get_book(typ="isbn", isbn="isbn:1234")
    rsp = books[0]
    rsp_code = books[1]
    assert rsp == common_response.DATABASE_ERROR[0]
    assert rsp_code == common_response.DATABASE_ERROR[1]


@mock.patch("app.model.books.Books.get_book_by_title")
def test_get_book_by_book_title_failed_book_not_found(mock_books):
    mock_books.return_value = []
    books = get_book(typ="title", title="Principles")
    rsp = books[0]
    rsp_code = books[1]
    print(books)
    assert rsp == {
        "status": "failed",
        "error_message": "not found"
    }
    assert rsp_code == 404


@mock.patch("app.model.books.Books.get_book_by_isbn")
def test_get_book_by_isbn_failed_book_not_found(mock_books):
    mock_books.return_value = []
    books = get_book(typ="isbn", isbn="1234")
    rsp = books[0]
    rsp_code = books[1]
    print(books)
    assert rsp == {
        "status": "failed",
        "error_message": "not found"
    }
    assert rsp_code == 404
