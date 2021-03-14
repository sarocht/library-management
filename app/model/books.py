from .. import db
from datetime import datetime


class Books(db.Model):
    """
    Books model
    """

    isbn = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    publisher_date = db.Column(db.DateTime, default=datetime.utcnow())
    page_count = db.Column(db.Integer, nullable=False)
    info_link = db.Column(db.String(100))
    status = db.Column(db.String(20), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return "<books(isbn='%s', title='%s')"

