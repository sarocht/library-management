from flask import Flask


def create_app() -> Flask:
    """
        Create flask application
    """
    app = Flask(__name__)

    from app.controllers.books import books_bp
    from app.migration.db import db_bp

    app.register_blueprint(books_bp)
    app.register_blueprint(db_bp)

    return app
