from .. import db
from datetime import datetime, date
from sqlalchemy.exc import SQLAlchemyError


class History(db.Model):
    """
    Book history model
    """
    transaction_id = db.Column(db.String(36), primary_key=True, unique=True)
    isbn = db.Column(db.String(50))
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow())
    action = db.Column(db.String(50))
    created_by = db.Column(db.String(50))
    borrowed_by = db.Column(db.String(50))

    def __repr__(self):
        return "<transaction(transaction_id='%s', isbn='%s', created_by='%s', borrowed_by='%s')" \
               % (self.transaction_id, self.isbn, self.created_by, self.borrowed_by)

    @staticmethod
    def borrow(transaction_id: str, isbn: str, transaction_date: datetime,
               action: str, created_by: str, borrowed_by: str):
        try:
            db.session.add(
                History(
                    transaction_id=transaction_id,
                    isbn=isbn,
                    transaction_date=transaction_date,
                    action=action,
                    created_by=created_by,
                    borrowed_by=borrowed_by
                )
            )
            db.session.commit()
        except SQLAlchemyError as e:
            return e

    @staticmethod
    def delete(transaction_id: str):
        try:
            book = db.session.query(History).filter_by(transaction_id=transaction_id).first()
            db.session.delete(book)
            db.session.commit()
        except SQLAlchemyError as e:
            return e