from flask import Blueprint, request
from app.service import history_service

history_bp = Blueprint("history_app", __name__)


@history_bp.route("/history", methods=["GET"])
def search_book_history():
    return history_service.search(
        typ=request.args.get("typ"),
        isbn=request.args.get("isbn"),
        title=request.args.get("title")
    )

