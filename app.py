# remote imports
from flask import request, make_response
from flask_restful import Resource
from datetime import datetime

# local imports
from config import app, db, api, ipdb
from models import Book, User

@app.route("/")
def home():
    return '<h1>Library API</h1>'

class Books(Resource):
    def get(self):
        books = [b.to_dict() for b in Book.query.all()]
        return make_response(
            books,
            200
        )
api.add_resource(Books, '/books')

# helper function to check if user is a librarian
def is_librarian(user):
    return user.is_librarian

class AddBook(Resource):
    def post(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        try:
            if not user:
                return make_response({'error': 'User not found'}, 404)
            if not is_librarian(user):
                return make_response({'error': 'Only librarians can add books'}, 403)
            isbn_number = request.json.get('isbn_number')
            title = request.json.get('title')
            book = Book(isbn_number=isbn_number, title=title)
            db.session.add(book)
            db.session.commit()
            return make_response(
                book.to_dict(),
                201
            )
        except ValueError as v_error:
            return make_response({'error': str(v_error)}, 400)
        except Exception as e:
            return make_response({'error': str(e)}, 400)
api.add_resource(AddBook, '/users/<int:user_id>/add_book')

class DeleteBook(Resource):
    def delete(self, user_id, book_id):
        user = User.query.filter_by(user_id=user_id).first()
        try:
            if not user:
                return make_response({'error': 'User not found'}, 404)
            if not is_librarian(user):
                return make_response({'error': 'Only librarians can delete books'}, 403)
            book = Book.query.filter_by(book_id=book_id).first()
            if not book:
                return make_response({'error': 'Book not found'}, 404)
            db.session.delete(book)
            db.session.commit()
            return make_response(
                'Book deleted successfully',
                204
            )
        except ValueError as v_error:
            return make_response({'error': str(v_error)}, 400)
        except Exception as e:
            return make_response({'error': str(e)}, 400)
api.add_resource(DeleteBook, '/users/<int:user_id>/delete_book/<int:book_id>')

class OverdueBooks(Resource):
    def get(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return make_response({'error': 'User not found'}, 404)
        if not is_librarian(user):
            return make_response({'error': 'Only librarians can view overdue books'}, 403)
        overdue_books = [b.to_dict() for b in Book.query.filter_by(overdue=True).all()]
        return make_response(
            overdue_books,
            200
        )
api.add_resource(OverdueBooks, '/users/<int:user_id>/overdue_books')

class CheckOutBook(Resource):
    def patch(self, book_id, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        try:
            if not user:
                return make_response({'error': 'User not found'}, 404)
            book = Book.query.filter_by(book_id=book_id).first()
            if not book:
                return make_response({'error': 'Book not found'}, 404)
            # checks if book is not checked out already
            if not book.checked_out:
                # checks if user has 3 books checked out
                users_checked_out_books = Book.query.filter_by(
                    checked_out_by=user_id).all()
                if len(users_checked_out_books) >= 3:
                    return make_response({'error': 'Can not check out more than 3 books at a time'}, 400)
                # checks if user has overdue books
                users_overdue_books = Book.query.filter_by(
                    checked_out_by=user_id, overdue=True).all()
                if len(users_overdue_books) > 0:
                    return make_response({'error': 'Can not check out a book if user has an overdue book'}, 400)
                book.checked_out = True
                book.checkout_date = datetime.utcnow()
                book.checked_out_by = user_id
                db.session.commit()
                return make_response(f'Book #{book_id} checked out by user #{user_id}', 200)
            else:
                return make_response({'error': 'Book already checked out'}, 400)
        except ValueError as v_error:
            return make_response({'error': str(v_error)}, 400)
        except Exception as e:
            return make_response({'error': str(e)}, 400)    
api.add_resource(CheckOutBook, '/users/<int:user_id>/books/<int:book_id>/checkout')

class ReturnBook(Resource):
    def patch(self, book_id, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        try:
            if not user:
                return make_response({'error': 'User not found'}, 404)
            book = Book.query.filter_by(book_id=book_id).first()
            if not book:
                return make_response({'error': 'Book not found'}, 404)
            # checks that book is checked out
            if not book.checked_out:
                return make_response({'error': 'Book not checked out'}, 400)
            # checks that user is the one who checked out the book
            if book.checked_out_by != user_id:
                return make_response({'error': 'Book checked out by another user'}, 400)
            else:
                book.checked_out = False
                book.checked_out_by = None
                db.session.commit()
                return make_response(f'Book #{book_id} returned by user #{user_id}', 200)
        except ValueError as v_error:
            return make_response({'error': str(v_error)}, 400)
        except Exception as e:
            return make_response({'error': str(e)}, 400)
api.add_resource(ReturnBook, '/users/<int:user_id>/books/<int:book_id>/return')

class UsersBooks(Resource):
    def get(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return make_response({'error': 'User not found'}, 404)
        books = [b.to_dict() for b in Book.query.filter_by(checked_out_by=user_id).all()]
        return make_response(
            books,
            200
        )
api.add_resource(UsersBooks, '/users/<int:user_id>/checked_out_books')


if __name__ == '__main__':
    app.run(port=5555, debug=True)