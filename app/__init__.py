from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app() -> Flask:
    """
        Create flask application
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:mysecretpassword@localhost:5432/postgres'
    db.init_app(app)

    from app.controller.books_controller import books_bp
    from app.migration.db import db_bp

    app.register_blueprint(books_bp)
    app.register_blueprint(db_bp)

    return app
