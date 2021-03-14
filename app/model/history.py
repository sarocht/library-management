from .. import db
from datetime import datetime


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
