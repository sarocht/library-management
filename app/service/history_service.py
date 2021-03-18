from app.model.history import History
from app.helper import common_response


def search(typ: str, isbn: str, title: str):
    """
        search book history by isbn or title
    """
    if typ not in ["isbn", "title"]:
        return {
            "status": "failed",
            "error_message": "invalid typ"
        }, 400

    if typ == "isbn":
        try:
            history = History.search_history_by_isbn(isbn)
        except Exception as e:
            return {'e': str(e)}
        if not history:
            return common_response.BOOK_NOT_FOUND
    else:
        try:
            history = History.search_history_by_title(title)
        except:
            return common_response.DATABASE_ERROR
        if not history:
            return common_response.BOOK_NOT_FOUND

    return {"history": history}
