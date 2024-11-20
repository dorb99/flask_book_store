from flask import Blueprint, request, abort
from models import BookCreateSchema, BookUpdateSchema
from marshmallow import ValidationError

book_schema = BookCreateSchema()
book_update_schema = BookCreateSchema()

# Create a blueprint for books CRUD
books_bp = Blueprint('books', __name__, url_prefix="/books")

books_db = [{"title": "1984", "author": 4, "pages": 345, "id": 0}]

@books_bp.route("", methods=['GET'])
def get_all_books():
    # Get all books from the DB
    if len(books_db) >= 0:
        return {"books": books_db}, 200
    else: 
        abort(404)
    
@books_bp.route("", methods=['POST'])
def create_books():
    try:
    # Create another book
        data = request.json
        book = {
            "title": data["title"],
            "author": data["author"],
            "pages": data["pages"],
            "id": len(books_db)
        }
        validated_book = book_schema.load(book)
        books_db.append(validated_book)
        return {"message": "Book created successfully", "book": validated_book}, 201
    except ValidationError as ve:
        return (f"Validation error: {str(ve)}")
         
        
@books_bp.route("<int:id>", methods=['GET'])
def get_book(id):
    # Get a specific book from the DB
    book = [book for book in books_db if book["id"] == id]
    if not book:
        abort(404)
    if len(book) == 1:
        return {"book": book[0]}
    else:
        return {"message": "More than one book found with the same ID"}, 409


@books_bp.route("<int:id>", methods=['PUT'])
def update_book(id):
    try:
        # Update a specific book from the DB
        data = request.json
        validated_book = book_update_schema.load(data)
        book = [book for book in books_db if validated_book["id"] == id]
        if not book:
            return {"message": "Book not found"}, 404
        if len(book) == 1:
            # option 1:
            for key, value in validated_book.items():
                book[0][key] = value
            # option 2 for dictionary:    
            # book.update(data)
            return {"message": "Book updated", "book": book}, 200    
        else:
            return {"message": "More than one book found with the same ID"}, 409
    
    except ValidationError as ve:
        return (f"Validation error: {str(ve)}")
    

@books_bp.route("<int:id>", methods=['DELETE'])
def delete_book(id):
    # Delete a specific book fro, the DB
    book = [book for book in books_db if book["id"] == id]
    if not book:
        return {"message": "Book not found"}, 404
    if len(book) == 1:
        books_db.remove(book[0])
        return {"message": "Book deleted successfully"}, 200
    else:
        return {"message": "More than one book found with the same ID"}, 409
        
