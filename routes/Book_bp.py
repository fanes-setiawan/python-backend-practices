from flask import Blueprint
from controllers.BookController import get_books, get_book , update_book, patch_book,delete_book, add_book

book_bp = Blueprint('Book_bp', __name__)


#get all book
book_bp.route('/api/books',methods=['GET'])(get_books)

#get by id
book_bp.route('/api/books/<int:book_id>',methods=['GET'])(get_book)

#add new book
book_bp.route('/api/book',methods=['POST'])(add_book)

#update book
book_bp.route('/api/books/<int:book_id>',methods=['PUT'])(update_book)

#partially update a book (patch)
book_bp.route('/api/books/<int:book_id>', methods=['PATCH'])(patch_book)

#delete book
book_bp.route('/api/books/<int:book_id>',methods=['DELETE'])(delete_book)


