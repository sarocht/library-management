from flask import Blueprint, request
from flask_expects_json import expects_json

from app.service import books_service
from app.schema.books import add_book_schema

books_bp = Blueprint("books_app", __name__)


@books_bp.route("/book", methods=["POST"])
@expects_json(add_book_schema)
def add_book():
    data = request.get_json()
    books_service.add_book(data.get("type"), data.get("isbn"), data.get("book_name"))
    return "ADD BOOK"


@books_bp.route("/book", methods=["GET"])
def get_book():
    # TODO
    return "GET BOOK"


@books_bp.route("/book", methods=["PUT"])
def update_book():
    # TODO
    return "UPDATE BOOK"


@books_bp.route("/book", methods=["DELETE"])
def delete_book():
    # TODO
    return "DELETE BOOK"


@books_bp.route("/books", methods=["GET"])
def get_books():
    # TODO
    return "GET BOOKS"





