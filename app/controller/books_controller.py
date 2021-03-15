from flask import Blueprint, request
from flask_expects_json import expects_json

from app.service import books_service
from app.schema.books import *

books_bp = Blueprint("books_app", __name__)


@books_bp.route("/book", methods=["POST"])
@expects_json(add_book_schema)
def add_book():
    _input = request.get_json()
    return books_service.add_book(isbn=_input.get("isbn"))


@books_bp.route("/book", methods=["GET"])
def get_book():
    return books_service.get_book(
        typ=request.args.get("typ"),
        isbn=request.args.get("isbn"),
        title=request.args.get("title")
    )


@books_bp.route("/book", methods=["PUT"])
@expects_json(update_book_schema)
def update_book():
    _input = request.get_json()
    return books_service.update_book(_input)


@books_bp.route("/book", methods=["DELETE"])
@expects_json(delete_book_schema)
def delete_book():
    _input = request.get_json()
    return books_service.delete_book(isbn=_input.get("isbn"))


@books_bp.route("/books", methods=["GET"])
def get_books():
    return books_service.get_all_books()




