from flask import Flask , jsonify , request

app = Flask(__name__)

books = {
    1:{'id':1, 'title' : 'Python basic', 'author':'John doe' , 'year' :2020},
    2:{'id':2, 'title' : 'Flask for Beginners', 'author':'John Smith' , 'year' :2021}
}

users ={
    1:{'user_id' :1 ,'username':'fanes123' , 'password' :'admin123' ,'fullname':'fanes setiawan','status':'mahasiswa'},
    2:{'user_id' :2 ,'username':'admin321' , 'password' :'321admin' ,'fullname':'adminadmin','status':'admin'}
}

#get all book
@app.route('/books',methods=['GET'])
def get_books():
    return jsonify(books)

#get by id
@app.route('/books/<int:book_id>',methods=['GET'])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        return jsonify({'error' : 'Book not found'}),404
    return jsonify(book)

#add new book
@app.route('/books',methods=['POST'])
def add_book():
    new_book = request.get_json()
    new_id = max(books.keys())+1
    books[new_id] = new_book
    return jsonify({'message' : 'Book added successfully!','book':new_book}),201

#update book
@app.route('/books/<int:book_id>',methods=['PUT'])
def update_book(book_id):
    update_book = request.get_json()
    book = books.get(book_id)
    if not book:
        return jsonify({'error':'Book not found'}),404
    update_book['id'] = book_id
    books[book_id] = update_book
    return jsonify({'message' : 'Book update successfully!','book' :update_book})

#partially update a book (patch)
@app.route('/books/<int:book_id>', methods=['PATCH'])
def patch_book(book_id):
    book = books.get(book_id)
    if not book:
        return jsonify({'error' : 'Book not fount'}),404

    patch_data = request.get_json()
    for key, value in patch_data.items():
        if key in book:
          book[key] = value
    
    return jsonify({'message':'Book partially updated successfully!','book':book})

#delete book
@app.route('/books/<int:book_id>',methods=['DELETE'])
def delete_book(book_id):
    book = books.pop(book_id, None)
    if not book:
        return jsonify({'error' : 'Book not fount'}),404
    return jsonify({'message':'Book deleted successfully!'})

#<----- user ----->

#get all user
@app.route('/users',methods=['GET'])
def get_users():
    return jsonify(users)

#get by id
@app.route('/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error' : 'user not found'}),404
    return jsonify(user)

#add new user
@app.route('/users',methods=['POST'])
def add_user():
    new_user = request.get_json()
    new_id = max(users.keys())+1
    users[new_id] = new_user
    return jsonify({'message' : 'user added successfully!','user':new_user}),201

#update user
@app.route('/users/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    update_user = request.get_json()
    user = users.get(user_id)
    if not user:
        return jsonify({'error':'user not found'}),404
    update_user['id'] = user_id
    users[user_id] = update_user
    return jsonify({'message' : 'user update successfully!','user' :update_user})

#partially update a user (patch)
@app.route('/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error' : 'user not fount'}),404

    patch_data = request.get_json()
    for key, value in patch_data.items():
        if key in user:
          user[key] = value
    
    return jsonify({'message':'user partially updated successfully!','user':user})

#delete user
@app.route('/users/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    user = users.pop(user_id, None)
    if not user:
        return jsonify({'error' : 'user not fount'}),404
    return jsonify({'message':'user deleted successfully!'})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error' : 'Not Found'}),404

if __name__ == '__main__':
    app.run(debug=True)
