from flask import Blueprint

db_bp = Blueprint('migration', __name__)


@db_bp.cli.command('db')
def migrate():
    """
        migrate db
    """
    # TODO
    pass
