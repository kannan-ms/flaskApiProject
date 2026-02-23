from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory database (list of dictionaries)
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 3, "title": "Force","author":"Kannan"}
]
# This is a test comment for Git practice
# Homepage Route (to avoid 404 on root)
@app.route('/')
def home():
    return "Welcome to the Book Library API! Try accessing <a href='/books'>/books</a> to see the data."

# 1. GET Request - Get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# 2. GET Request - Get a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

# 3. POST Request - Create a new book
@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.get_json()
    
    # Simple validation using ID generation logic based on last item
    new_id = books[-1]["id"] + 1 if books else 1
    new_book["id"] = new_id
    
    books.append(new_book)
    return jsonify(new_book), 201

# 4. PUT Request - Update an existing book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    data = request.get_json()
    book.update(data)
    return jsonify(book)

# 5. DELETE Request - Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
