from flask import Flask, request, jsonify;
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://dbAdmin:rMhSiXkrdxTgoLxX@dbprac.x8dctco.mongodb.net/BookCatlog?retryWrites=true&w=majority"
db = PyMongo(app).db

@app.route("/")
def getAllBooks():
    books = db["books"].find({})
    book_list = []

    for book in books:
        book_list.append({
            'id' : str(book['_id']),
            'title': book['title'],
            'author': book['author'],
            'brief_summary': book['brief_summary'],
            'cover_image': book['cover_image'],
            'genre': book['genre'],
            'publication_date': book['publication_date'],
            'free_or_paid': book['free_or_paid']
    })

    return jsonify(book_list)

# book by ID
@app.route("/<book_id>", methods=["GET"])
def getBook(book_id):
    temp = db["books"].find_one({
        '_id' : ObjectId(book_id)
    })

    book = {
        'id': str(temp['_id']),
        'title': temp['title'],
        'author': temp['author'],
        'brief_summary': temp['brief_summary'],
        'cover_image': temp['cover_image'],
        'genre': temp['genre'],
        'publication_date': temp['publication_date'],
        'free_or_paid': temp['free_or_paid']
    }

    return jsonify(book)

# get book by name
@app.route("/<book_title>", methods=["GET"])
def getBookByTitle(book_title):

    temp = db["books"].find_one({
        'title' : book_title
    })
    
    book = {
        'title': temp['title'],
        'author': temp['author'],
        'brief_summary': temp['brief_summary'],
        'cover_image': temp['cover_image'],
        'genre': temp['genre'],
        'publication_date': temp['publication_date'],
        'free_or_paid': temp['free_or_paid']
    }

    return jsonify(book)

# search book by author or title
@app.route("/searchBook", methods=["GET"])
def getBooks():
    search_query = "Pride and Prejudice"
    books = db["books"].find({
        '$or' : [
            {"title": {"$regex": search_query, "$options":"i"}},
            {"author": {"$regex": search_query, "$options":"i"}},
        ]
    })

    book_list = []

    for book in books:
        book_list.append({
            'title': book['title'],
            'author': book['author'],
            'brief_summary': book['brief_summary'],
            'cover_image': book['cover_image'],
            'genre': book['genre'],
            'publication_date': book['publication_date'],
            'free_or_paid': book['free_or_paid']
        })

    return jsonify(book_list)

# book by ID
@app.route("/book/<book_id>", methods=["GET"])
def getBookById(book_id):
    book = db["books"].find_one({
        '_id' : ObjectId(book_id)
    })

    return jsonify(book)

# create new book
@app.route('/add_book', methods=['POST'])
def add_book():
    data = request.get_json()
    print(data)
    new_book = {
        'title': data['title'],
        'author': data['author'],
        'brief_summary': data['brief_summary'],
        'cover_image': data['cover_image'],
        'genre': data['genre'],
        'publication_date': data['publication_date'],
        'free_or_paid': data['free_or_paid']
    }

    db["books"].insert_one(new_book)
    return jsonify({'message': 'Book added successfully!'})
    
# update existing book
@app.route('/update_book/<book_id>', methods=['PATCH'])
def update_book(book_id):
    data = request.get_json()

    updated_book = {
        'title': data['title'],
        'author': data['author'],
        'brief_summary': data['brief_summary'],
        'cover_image': data['cover_image'],
        'genre': data['genre'],
        'publication_date': data['publication_date'],
        'free_or_paid': data['free_or_paid']
    }

    result = db["books"].find_one_and_update({'_id': book_id}, {'$set': updated_book})
    print(result)

    if result.modified_count == 1:
        return jsonify({'message': 'Book updated successfully!'}), 200
    else:
        return jsonify({'message': 'No book was updated.'}), 200

app.run(debug=True)
