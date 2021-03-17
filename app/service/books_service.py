from app.model.books import Books
from app.model.history import History
from app.external_api.google_books import GoogleBookAPI

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
        if Books.get_book_by_isbn(isbn):
            return {
                "status": "failed",
                "error_message": "book already exists"
            }
    except:
        return {
            "status": "failed",
            "error_message": "database error"
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


def get_book(typ: str, isbn: str, title: str):
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
            if not books:
                return {
                    "status": "failed",
                    "error_message": "not found"
                }, 404
        except Exception as e:
            return {
                "status": "failed",
                "error_message": "database error"
            }
    else:
        try:
            books = Books.get_book_by_title(title)
            if not books:
                return {}, 404
        except Exception as e:
            return {
                "status": "failed",
                "error_message": "database error"
            }

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
        return {
            "status": "failed",
            "error_message": "database error"
        }, 500

    return {
        "status": "success"
    }


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
    return {
        "status": "success"
    }


def get_all_books():
    """
        Get all books in library
    """
    try:
        books = Books.get_all_books()
    except:
        return {
            "status": "failed",
            "error_message": "database error"
        }

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
        return {
            "status": "failed",
            "error_message": "database error"
        }

    if len(book) == 0:
        return {
            "status": "failed",
            "error_message": "Book does not exists in library"
        }
    if book[0].get("status") != "Available":
        return {
            "status": "failed",
            "error_message": "Book is not available"
        }

    try:
        Books.update_book(isbn=book[0]['isbn'], status="Borrowed")
    except Exception as e:
        return {
            "status": "failed",
            "error_message": "database error"
        }

    try:
        History.borrow(
            transaction_id=str(uuid.uuid4()),
            isbn=isbn,
            transaction_date=datetime.utcnow(),
            action="Borrowed",
            created_by=created_by,
            borrowed_by=borrowed_by
        )
    except:
        # Rollback
        Books.update_book(isbn=book.isbn, status="Available")
        return {
            "status": "failed",
            "error_message": "database error"
        }

    return {
        "status": "success",
        "error_message": ""
    }