#remote imports
from datetime import timedelta, datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import event
#local imports
from config import db

class Book(db.Model, SerializerMixin):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    isbn_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    checkout_date = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    checked_out = db.Column(db.Boolean, default=False)
    overdue = db.Column(db.Boolean, default=False)
    checked_out_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    def __repr__(self):
        return f"<Book #{self.book_id}: isbn_number: {self.isbn_number}, title: {self.title}, checked_out: {self.checked_out}, checked_out_by: user{self.checked_out_by}, overdue: {self.overdue}>"
    
def set_due_date_and_overdue(mapper, connection, target):
    if target.checked_out:
        # target.checkout_date = datetime.utcnow()
        target.due_date = target.checkout_date + timedelta(weeks=2)
        target.overdue = datetime.utcnow() > target.due_date
    else:
        target.checkout_date = None
        target.due_date = None
        target.overdue = False

event.listen(Book, 'before_insert', set_due_date_and_overdue)
event.listen(Book, 'before_update', set_due_date_and_overdue)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    is_librarian = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User #{self.user_id}, is_librarian={self.is_librarian}>"