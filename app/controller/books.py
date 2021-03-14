from flask import Blueprint

books_bp = Blueprint("books_app", __name__)


@books_bp.route("/book", methods=["POST"])
def add_book():
    # TODO
    return "ADD BOOK"


@books_bp.route("/book/", methods=["GET"])
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





