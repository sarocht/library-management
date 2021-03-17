from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.helper import config

db = SQLAlchemy()


def create_app() -> Flask:
    """
        Create flask application
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.POSTGRES_DATABASE_URI
    db.init_app(app)

    from app.controller.books_controller import books_bp
    from app.migration.db import db_bp

    app.register_blueprint(books_bp)
    app.register_blueprint(db_bp)

    return app
