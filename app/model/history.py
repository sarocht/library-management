from .. import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_serializer import SerializerMixin


class History(db.Model, SerializerMixin):
    """
    Book history model
    """
    transaction_id = db.Column(db.String(36), primary_key=True, unique=True)
    isbn = db.Column(db.String(50))
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow())
    action = db.Column(db.String(50))
    created_by = db.Column(db.String(50))
    action_by = db.Column(db.String(50))

    def __repr__(self):
        return "<transaction(transaction_id='%s', isbn='%s', created_by='%s', action_by='%s')" \
               % (self.transaction_id, self.isbn, self.created_by, self.action_by)

    @staticmethod
    def add(transaction_id: str, isbn: str, transaction_date: datetime,
            action: str, created_by: str, action_by: str):
        try:
            db.session.add(
                History(
                    transaction_id=transaction_id,
                    isbn=isbn,
                    transaction_date=transaction_date,
                    action=action,
                    created_by=created_by,
                    action_by=action_by
                )
            )
            db.session.commit()
        except SQLAlchemyError as e:
            return e

    @staticmethod
    def delete(transaction_id: str):
        try:
            history = db.session.query(History).filter_by(transaction_id=transaction_id).first()
            db.session.delete(history)
            db.session.commit()
        except SQLAlchemyError as e:
            return e

    @staticmethod
    def search_history_by_isbn(isbn: str):
        try:
            history = db.session.query(History).filter_by(isbn=isbn).all()
        except SQLAlchemyError as e:
            return e
        return [h.to_dict() for h in history]

    @staticmethod
    def search_history_by_title(title: str):
        try:
            history = db.session.query(History).filter_by(title=title).all()
        except SQLAlchemyError as e:
            return e
        return [h.to_dict() for h in history]
