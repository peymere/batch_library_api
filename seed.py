#local imports
from config import db
from models import Book, User
from app import app
from datetime import datetime, timedelta

def seed_users():
    user_data = [
        User(is_librarian=True),
        User(is_librarian=False),
        User(is_librarian=False),
        User(is_librarian=False),
        User(is_librarian=False)
    ]
    return user_data

def seed_books():
    book_data = [
        Book(
            isbn_number=10553381687, 
            title='A Game of Thrones',
            checkout_date=datetime.utcnow() - timedelta(days=14),
            checked_out=True,
            checked_out_by=2),

        Book(isbn_number=10553108034, 
            title='A Clash of Kings',
            checkout_date=datetime.utcnow(),
            checked_out=True,
            checked_out_by=3),
        Book(isbn_number=10553106635, title='A Storm of Swords'),
        Book(isbn_number=10553801503, title='A Feast for Crows'),
        Book(isbn_number=10006486118, title='A Dance with Dragons'),
        Book(isbn_number=10027000303, title='Watership Down',
            checkout_date=datetime.utcnow() - timedelta(days=7),
            checked_out=True,
            checked_out_by=4),
        Book(isbn_number=10553381687, 
            title='A Game of Thrones',
            checkout_date=datetime.utcnow(),
            checked_out=True,
            checked_out_by=4),
        Book(isbn_number=10553108034,
            title='A Clash of Kings',
            checkout_date=datetime.utcnow() - timedelta(days=5),
            checked_out=True,
            checked_out_by=4),
    ]
    return book_data

if __name__ == '__main__':
    with app.app_context():
        print('Clearing database...')
        User.query.delete()
        Book.query.delete()

        print('Seeding users...')
        users = seed_users()
        db.session.add_all(users)
        db.session.commit()

        print('Seeding books...')
        books = seed_books()
        db.session.add_all(books)
        db.session.commit()

        print('Database seeded!')

