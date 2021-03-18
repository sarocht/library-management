from flask import Blueprint
from .. import db

db_bp = Blueprint('migration', __name__)


@db_bp.cli.command('createtables')
def create_db():
    """
       create database
    """
    from app.model.books import Books
    from app.model.history import History
    db.create_all()


@db_bp.cli.command('droptables')
def drop_db():
    """
        drop database
    """
    from app.model.books import Books
    from app.model.history import History
    db.drop_all()
