#remote imports
from datetime import timedelta, datetime

#local imports
from config import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    isbn_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    checkout_date = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    checked_out = db.Column(db.Boolean, default=False)
    overdue = db.Column(db.Boolean, default=False)
    checked_out_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f"<Book #{self.id}: isbn_number={self.isbn_number}, title={self.title}, checked_out={self.checked_out}, checked_out_by=user{self.checked_out_by}, overdue={self.overdue}>"



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    is_librarian = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User #{self.id}, is_librarian={self.is_librarian}>"