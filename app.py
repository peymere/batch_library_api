# remote imports
from flask import request, make_response, session
from flask_restful import Resource


# local imports
from config import app, db, api
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

    def post(self):
        data = request.get_json()
        try:
            new_book = Book(
                isbn_number=data['isbn_number'],
                title=data['title']
            )
        except ValueError as v_error:
            return make_response({'error': [str(v_error)]}, 400)
        db.session.add(new_book)
        db.session.commit()
        return make_response(
            new_book.to_dict(),
            201
        )
api.add_resource(Books, '/books')

class OverdueBooks(Resource):
    def get(self):
        overdue_books = [b.to_dict() for b in Book.query.filter_by(overdue=True).all()]
        return make_response(
            overdue_books,
            200
        )
api.add_resource(OverdueBooks, '/books/overdue')

class BookById(Resource):
    def get(self, id):
        book = Book.query.filter_by(id=id).first()
        if not book:
            return make_response({'error': 'Book not found'}, 404)
        return make_response(
            book.to_dict(), 
            200
        )
    
    def delete(self, id):
        book = Book.query.filter_by(id=id).first()
        if not book:
            return make_response({'error': 'Book not found'}, 404)
        db.session.delete()
        db.session.commit()
        return make_response(
            'deleted successfully',
            204
        )
api.add_resource(BookById, '/books/<int:id>')


class Users(Resource):
    def get(self):
        users = [u.to_dict() for u in User.query.all()]
        return make_response(
            users,
            200
        ) 
api.add_resource(Users, '/users')