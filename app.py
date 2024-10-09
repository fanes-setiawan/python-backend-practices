from flask import Flask , jsonify , request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# books = {
#     1:{'id':1, 'title' : 'Python basic', 'author':'John doe' , 'year' :2020},
#     2:{'id':2, 'title' : 'Flask for Beginners', 'author':'John Smith' , 'year' :2021}
# }

# users ={
#     1:{'user_id' :1 ,'username':'fanes123' , 'password' :'admin123' ,'fullname':'fanes setiawan','status':'mahasiswa'},
#     2:{'user_id' :2 ,'username':'admin321' , 'password' :'321admin' ,'fullname':'adminadmin','status':'admin'}
# }

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable =False)
    fullname = db.Column(db.String(100), nullable =False)
    status = db.Column(db.String(100) , nullable =False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'password' : self.password,
            'status': self.status
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
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

#get by id
@app.route('/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error' : 'user not found'}),404
    return jsonify(user.to_dict())

#add new user
@app.route('/users',methods=['POST'])
def add_user():
    new_user_data = request.get_json()
    new_user = User(
        username = new_user_data['username'],
        password = new_user_data['password'],
        fullname = new_user_data['fullname'],
        status = new_user_data['status']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message' : 'user added successfully!','user':new_user.to_dict()}),201

#update user
@app.route('/users/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error':'user not found'}),404
    update_data = request.get_json()
    user.username = update_data.get('username',user.username)
    user.password = update_data.get('password',user.password)
    user.fullname = update_data.get('fullname',user.fullname)
    user.status = update_data.get('status',user.status)
    
    db.session.commit()
    return jsonify({'message' : 'user update successfully!','user' :user.to_dict()})

#partially update a user (patch)
@app.route('/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error' : 'user not fount'}),404

    patch_data = request.get_json()
    if 'username' in patch_data:
        user.usename = patch_data['username']
        
    if 'password' in patch_data:
        user.password = patch_data['password']
        
    if 'fullname' in patch_data:
        user.fullname = patch_data['fullname']
        
    if 'status' in patch_data:
        user.status = patch_data['status']
        
    db.session.commit()
    return jsonify({'message':'user partially updated successfully!','user':user.to_dict()})

#delete user
@app.route('/users/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error' : 'user not fount'}),404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'user deleted successfully!'})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error' : 'Not Found'}),404

if __name__ == '__main__':
    app.run(debug=True , port=5000)
