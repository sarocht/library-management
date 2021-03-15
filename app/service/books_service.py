from app.model.books import Books
from app.external_api.google_books import GoogleBookAPI

from datetime import datetime, date
from dictor import dictor
from typing import Dict


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
                "error_message": str(e)
            }
    else:
        try:
            books = Books.get_book_by_title(title)
            if not books:
                return {}, 404
        except Exception as e:
            return {
                "status": "failed",
                "error_message": str(e)
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