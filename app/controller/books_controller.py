from flask import Blueprint
from ..service import books_service

books_bp = Blueprint("books_app", __name__)


@books_bp.route("/book", methods=["POST"])
def add_book():
    # TODO
    books_service.add_book()
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





