from flask import Flask , jsonify , request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# books = {
#     1:{'id':1, 'title' : 'Python basic', 'author':'John doe' , 'year' :2020},
#     2:{'id':2, 'title' : 'Flask for Beginners', 'author':'John Smith' , 'year' :2021}
# }

users ={
    1:{'user_id' :1 ,'username':'fanes123' , 'password' :'admin123' ,'fullname':'fanes setiawan','status':'mahasiswa'},
    2:{'user_id' :2 ,'username':'admin321' , 'password' :'321admin' ,'fullname':'adminadmin','status':'admin'}
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://pwl123:2wsx1qaz@localhost:3306/db_repository_0627'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#model book menggunakan sqlalchemy orm
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            'id':self.id,
            'title':self.title,
            'author':self.author,
            'year':self.year
        }

#init database
@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()

#get all book
@app.route('/books',methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

#get by id
@app.route('/books/<int:book_id>',methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error' : 'Book not found'}),404
    return jsonify(book.to_dict())

#add new book
@app.route('/books',methods=['POST'])
def add_book():
    new_book_data = request.get_json()
    new_book = Book(
        title = new_book_data['title'],
        author = new_book_data['author'],
        year = new_book_data['year']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message' : 'Book added successfully!','book':new_book.to_dict()}),201

#update book
@app.route('/books/<int:book_id>',methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error':'Book not found'}),404
    updated_data = request.get_json()
    book.title = updated_data.get('title',book.title)
    book.author = updated_data.get('author',book.author)
    book.year = updated_data.get('year', book.year)
    
    db.session.commit()
    return jsonify({'message' : 'Book update successfully!','book' :book.to_dict()})

#partially update a book (patch)
@app.route('/books/<int:book_id>', methods=['PATCH'])
def patch_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error' : 'Book not fount'}),404

    patch_data = request.get_json()
    if 'title' in patch_data:
       book.title = patch_data['title']
    if 'author' in patch_data:
       book.author = patch_data['author']
    if 'year' in patch_data:
       book.year = patch_data['year']
    
    db.session.commit()
    return jsonify({'message':'Book partially updated successfully!','book':book.to_dict()})

#delete book
@app.route('/books/<int:book_id>',methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error' : 'Book not fount'}),404
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message':'Book deleted successfully!'})

#<----- user ----->

#get all user
@app.route('/users',methods=['GET'])
def get_users():
    users
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
    app.run(debug=True , port=5000)
