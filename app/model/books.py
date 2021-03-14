from .. import db
from datetime import date, datetime
from sqlalchemy.exc import SQLAlchemyError


class Books(db.Model):
    """
    Books model
    """

    isbn = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    published_date = db.Column(db.Date, default=date.today())
    page_count = db.Column(db.Integer, nullable=False)
    info_link = db.Column(db.String(100))
    status = db.Column(db.String(20), nullable=False)
    created_date = db.Column(db.Date, default=date.today())

    def __repr__(self):
        return "<books(isbn='%s', title='%s')" % (self.isbn, self.title)

    @staticmethod
    def add_book(isbn: str, title: str, subtitle: str, publisher: str,
                 published_date: date, page_count: int, info_link: str, status: str, created_date: date):
        try:
            db.session.add(
                Books(
                    isbn=isbn,
                    title=title,
                    subtitle=subtitle,
                    publisher=publisher,
                    page_count=page_count,
                    info_link=info_link,
                    status=status,
                )
            )
            db.session.commit()
        except SQLAlchemyError as e:
            return e
