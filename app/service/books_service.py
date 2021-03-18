from app.model.books import Books
from app.model.history import History
from app.external_api.google_books import GoogleBookAPI
from app.helper import common_response

from datetime import datetime, date
from dictor import dictor
from typing import Dict
import uuid


def add_book(isbn: str):
    """
        Add book into database
        the book name must be existing in Google Books
        and have only one in Google Books
    """
    try:
        book = Books.get_book_by_isbn(isbn)
    except:
        return common_response.DATABASE_ERROR

    if book:
        return {
            "status": "failed",
            "error_message": "book already exists"
        }

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
                Books.add_book(
                    isbn=isbn,
                    title=dictor(books, "items.0.volumeInfo.title"),
                    subtitle=dictor(books, "items.0.volumeInfo.subtitle"),
                    publisher=dictor(books, "items.0.volumeInfo.publisher"),
                    published_date=dictor(books, "items.0.volumeInfo.publishedDate"),
                    page_count=dictor(books, "items.0.volumeInfo.pageCount"),
                    info_link=dictor(books, "items.0.volumeInfo.infoLink"),
                    status="Available",
                    created_date=date.today()
                )
                return common_response.SUCCESS
            except:
                return common_response.DATABASE_ERROR

    return {
        "status": "failed",
        "error_message": "Invalid format from Google Book API"
    }, 500


def get_book(typ: str, isbn: str = "", title: str = ""):
    """
        Search books by isbn or book title
    """
    if typ not in ["isbn", "title"]:
        return {
            "status": "failed",
            "error_message": "invalid typ"
        }, 400

    if typ == "isbn":
        try:
            books = Books.get_book_by_isbn(isbn)
        except:
            return common_response.DATABASE_ERROR
        if not books:
            return common_response.BOOK_NOT_FOUND
    else:
        try:
            books = Books.get_book_by_title(title)
        except:
            return common_response.DATABASE_ERROR
        if not books:
            return common_response.BOOK_NOT_FOUND

    return {"books": books}


def update_book(book: Dict):
    """
        update book using isbn key
        Only existing field will by updated
    """

    try:
        if book.get("published_date"):
            book["published_date"] = datetime.strptime(book.get("published_date"), "%Y-%m-%d")
        if book.get("created_date"):
            book["created_date"] = datetime.strptime(book.get("created_date"), "%Y-%m-%d")
        if book.get("status") and book["status"] not in ["Borrow", "Available"]:
            return {
                "status": "failed",
                "error_message": "Invalid status"
            }, 404
    except:
        return {
            "status": "failed",
            "error_message": "cannot convert string to date format"
        }, 404

    try:
        Books.update_book(
            isbn=book["isbn"],
            title=book.get("title"),
            subtitle=book.get("subtitle"),
            publisher=book.get("publisher"),
            published_date=book.get("published_date"),
            page_count=book.get("page_count"),
            info_link=book.get("info_link"),
            status=book.get("status"),
            created_date=book.get("created_date")
        )
    except:
        return common_response.DATABASE_ERROR

    return common_response.SUCCESS


def delete_book(isbn: str):
    """
        Delete Book by isbn
    """
    try:
        Books.delete_book(isbn)
    except:
        return {
            "status": "failed",
            "error_message": "database error"
        }, 500
    return common_response.SUCCESS


def get_all_books():
    """
        Get all books in library
    """
    try:
        books = Books.get_all_books()
    except:
        return common_response.DATABASE_ERROR

    return {
        "books": books
    }


def borrow_book(isbn: str, created_by: str, borrowed_by: str):
    """
        Borrow the book
    """
    try:
        book = Books.get_book_by_isbn(isbn)
    except:
        return common_response.DATABASE_ERROR

    if len(book) == 0:
        return common_response.BOOK_NOT_FOUND
    if book[0].get("status") != "Available":
        return {
            "status": "failed",
            "error_message": "Book is not available"
        }

    try:
        Books.update_book(isbn=book[0]['isbn'], status="Borrowed")
    except Exception as e:
        return common_response.DATABASE_ERROR

    try:
        History.add(
            transaction_id=str(uuid.uuid4()),
            isbn=isbn,
            transaction_date=datetime.utcnow(),
            action="Borrowed",
            created_by=created_by,
            action_by=borrowed_by
        )
    except:
        # Rollback
        Books.update_book(isbn=book.isbn, status="Available")
        return common_response.DATABASE_ERROR

    return common_response.SUCCESS


def return_book(isbn: str, created_by: str, returned_by: str):
    """
        return book to library
    """
    try:
        book = Books.get_book_by_isbn(isbn)
    except:
        return common_response.DATABASE_ERROR

    if len(book) == 0:
        return common_response.BOOK_NOT_FOUND

    if book[0].get("status") != "Borrowed":
        return {
            "status": "failed",
            "error_message": "Book is not borrowed"
        }, 500

    try:
        Books.update_book(isbn=book[0]['isbn'], status="Available")
    except Exception as e:
        return common_response.DATABASE_ERROR

    try:
        History.add(
            transaction_id=str(uuid.uuid4()),
            isbn=isbn,
            transaction_date=datetime.utcnow(),
            action="Available",
            created_by=created_by,
            action_by=returned_by
        )
    except:
        # Rollback
        Books.update_book(isbn=book.isbn, status="Borrowed")
        return common_response.DATABASE_ERROR

    return common_response.SUCCESS