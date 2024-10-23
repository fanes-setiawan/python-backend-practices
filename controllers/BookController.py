from flask import jsonify, request
from models.BookModel import Book
from models.CategoryModel import Category
from config import db


def get_books():
    books = Book.query.all()
    books_with_categories = []
    for book in books:
        # get category
        category = Category.query.get(book.category_id)
        # add detail book
        books_with_categories.append(
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "description": book.description,
                "year": book.year,
                "category_name": category.name if category else "No Category",
            }
        )
    response = {
        "status": "success",
        "data": {"books": books_with_categories},
        "message": "Books retrieved successfully",
    }
    return jsonify(response), 200


def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "error", "message": "Book not found"}), 404

    # get category
    category = Category.query.get(book.category_id)
    book_data = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "description": book.description,
        "year": book.year,
        "category_name": category.name if category else "No Category",
    }

    response = {
        "status": "success",
        "data": {"book": book_data},
        "message": "Book retrieved successfully!",
    }
    return jsonify(response), 200


def add_book():
    new_book_data = request.get_json()
    new_book = Book(
        title=new_book_data["title"],
        author=new_book_data["author"],
        year=new_book_data["year"],
        description=new_book_data.get("description", ""),
        category_id=new_book_data["category_id"],
    )
    db.session.add(new_book)
    db.session.commit()
    return (
        jsonify({"message": "Book added successfully!", "book": new_book.to_dict()}),
        201,
    )


def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    updated_data = request.get_json()
    book.title = updated_data.get("title", book.title)
    book.author = updated_data.get("author", book.author)
    book.year = updated_data.get("year", book.year)
    book.description = updated_data.get("description", book.description)
    book.category_id = updated_data.get("category_id", book.category_id)

    db.session.commit()
    return jsonify({"message": "Book update successfully!", "book": book.to_dict()})


def patch_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not fount"}), 404

    patch_data = request.get_json()
    if "title" in patch_data:
        book.title = patch_data["title"]
    if "author" in patch_data:
        book.author = patch_data["author"]
    if "year" in patch_data:
        book.year = patch_data["year"]
    if "description" in patch_data:
        book.description = patch_data["description"]
    if "category" in patch_data:
        # category isnotnull
        category = Category.query.get(patch_data["category_id"])
        if category:
            book.category_id = patch_data["category_id"]
        else:
            return jsonify({"error": "Category not found"}), 404

    db.session.commit()
    return jsonify(
        {"message": "Book partially updated successfully!", "book": book.to_dict()}
    )


def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not fount"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully!"})
