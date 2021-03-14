from flask import Blueprint
from .. import db

db_bp = Blueprint('migration', __name__)


@db_bp.cli.command('db')
def migrate():
    """
        migrate db
    """
    from app.model.books import Books
    from app.model.history import History
    db.create_all()
