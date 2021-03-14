from app.model.books import Books
from app.external_api.google_books import GoogleBookAPI

from datetime import datetime, date
from dictor import dictor


def add_book(isbn: str):
    """
        Add book into database
        the book name must be existing in Google Books
        and have only one in Google Books
    """
    try:
        books = GoogleBookAPI.search_books(query=isbn)
    except:
        return {
            "status": "failed",
            "error_message": "cannot make a request"
        }, 500

    if books.get("totalItems") == 0:
        return {
            "status": "failed",
            "error_message": "book not found in Google Books"
        }, 404

    elif books.get("totalItems") > 1:
        return {
            "status": "failed",
            "error_message": "Ambiguous"
        }, 400

    elif books.get("totalItems") == 1 and len(books.get("items")) == 1:

        if dictor(books, "items.0.volumeInfo.title") \
                and dictor(books, "items.0.volumeInfo.subtitle") \
                and dictor(books, "items.0.volumeInfo.publisher") \
                and dictor(books, "items.0.volumeInfo.publishedDate") \
                and dictor(books, "items.0.volumeInfo.pageCount") \
                and dictor(books, "items.0.volumeInfo.infoLink"):

            try:
                published_date = datetime.strptime(
                    dictor(books, "items.0.volumeInfo.publishedDate"),
                    "%Y-%m-%d"
                ).date()
                Books.add_book(
                    isbn=isbn,
                    title=dictor(books, "items.0.volumeInfo.title"),
                    subtitle=dictor(books, "items.0.volumeInfo.subtitle"),
                    publisher=dictor(books, "items.0.volumeInfo.publisher"),
                    published_date=published_date,
                    page_count=dictor(books, "items.0.volumeInfo.pageCount"),
                    info_link=dictor(books, "items.0.volumeInfo.infoLink"),
                    status="Available",
                    created_date=date.today()
                )
                return {
                    "status": "success",
                }, 200
            except Exception as e:
                return {
                    "status": "failed",
                    "error_message": "database error"
                }, 500

    return {
        "status": "failed",
        "error_message": "Invalid format from Google Book API"
    }, 500


def get_book():
    # TODO
    pass


def update_book():
    # TODO
    pass


def delete_book():
    # TODO
    pass


def get_books():
    # TODO
    pass
