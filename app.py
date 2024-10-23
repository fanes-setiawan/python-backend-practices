from flask import Flask , jsonify , request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://pwl123:2wsx1qaz@localhost:3306/db_repository_0627'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#model book menggunakan sqlalchemy orm
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255),nullable=True)
    category_id = db.Column(db.Integer , db.ForeignKey('category.id'),nullable=False)
    
    def to_dict(self):
        return {
            'id':self.id,
            'title':self.title,
            'author':self.author,
            'year':self.year,
            'description':self.description,
            'category_id':self.category_id
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable =False)
    fullname = db.Column(db.String(100), nullable =False)
    status = db.Column(db.String(100) , nullable =False)
    level_id = db.Column(db.Integer ,db.ForeignKey('level.id'), nullable =False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'password' : self.password,
            'status': self.status,
            'level_id': self.level_id
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False,unique=True)
    
    books = db.relationship('Book',backref='category',lazy=True)
    
    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name
        }
        
class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False,unique=True)
    
    users = db.relationship('User',backref='level',lazy=True)
    
    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name
        }

#init database
@app.before_request
def create_tables():
    app.before_request_funcs[None].remove(create_tables)
    db.create_all()


#BOOK ROUTE==========================================================================>

#get all book
@app.route('/books',methods=['GET'])
def get_books():
    books = Book.query.all()
    books_with_categories =[]
    for book in books:
        #get category
        category = Category.query.get(book.category_id)
        #add detail book 
        books_with_categories.append({
            'id':book.id,
            'title':book.title,
            'author':book.author,
            'description':book.description,
            'year':book.year,
            'category_name':category.name if category else "No Category"
        })
    response = {
        'status':'success',
        'data':{
            'books':books_with_categories
        },
        'message':'Books retrieved successfully'
    }
    return jsonify(response),200

#get by id
@app.route('/books/<int:book_id>',methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error' : 'error','message':'Book not found'}),404
    
    #get category
    category = Category.query.get(book.category_id)
    book_data = {
         'id':book.id,
         'title':book.title,
         'author':book.author,
         'description':book.description,
         'year':book.year,
         'category_name':category.name if category else "No Category"
    }
    
    response ={
        'status': 'success',
        'data':{
            'book':book_data
        },
        'message':'Book retrieved successfully!'
    }
    return jsonify(response),200

#add new book
@app.route('/books',methods=['POST'])
def add_book():
    new_book_data = request.get_json()
    new_book = Book(
        title = new_book_data['title'],
        author = new_book_data['author'],
        year = new_book_data['year'],
        description=new_book_data.get('description',''),
        category_id = new_book_data['category_id']
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
    book.description = updated_data.get('description', book.description)
    book.category_id = updated_data.get('category_id',book.category_id)
    
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
    if 'description' in patch_data:
        book.description = patch_data['description']
    if 'category' in patch_data:
        #category isnotnull
        category = Category.query.get(patch_data['category_id'])
        if category:
            book.category_id = patch_data['category_id']
        else:
            return jsonify({'error': 'Category not found'}),404
    
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

#USER ROUTE==========================================================================>

#get all user
@app.route('/users',methods=['GET'])
def get_users():
    users = User.query.all()
    users_with_level =[]
    for user in users:
        #get level
        level = Level.query.get(user.level_id)
        #add details
        users_with_level.append({
            'id': user.id,
            'username': user.username,
            'fullname': user.fullname,
            'password' : user.password,
            'status': user.status,
            'level_name': level.name if level else "No Level"
        })
        
    response ={
        'status':'success',
        'data':{
            'users':users_with_level
        },
        'message':'Users retrived successfully!'
    }
    return jsonify(response),200

#get by id
@app.route('/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error' : 'user not found'}),404
    
    #get level
    level = Level.query.get(user.level_id)
    user_data = {
        'id': user.id,
        'username': user.username,
        'fullname': user.fullname,
        'password' : user.password,
        'status': user.status,
        'level_name': level.name if level else "No Level"
    }
    
    response ={
        'status':'success',
        'data':{
            'user':user_data
        },
        'message':'User retrieved successfuly!'
    }
    return jsonify(response),200

#add new user
@app.route('/users',methods=['POST'])
def add_user():
    new_user_data = request.get_json()
    new_user = User(
        username = new_user_data['username'],
        password = new_user_data['password'],
        fullname = new_user_data['fullname'],
        status = new_user_data['status'],
        level_id = new_user_data['level_id']
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
    user.level_id = update_data.get('level_id',user.level_id)
    
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
    if 'level' in patch_data:
        level = Level.query.get(patch_data['level_id'])
        if level:
            user.level_id = patch_data['level_id']
        else:
            return jsonify({'error': 'Level not found'}),404
        
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


#CATEGORY ROUTE==========================================================================>

#get all category
@app.route('/category',methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

#get category by id
@app.route('/category/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'error':'Category not found'}),404
    return jsonify(category.to_dict())

#new category
@app.route('/category',methods=['POST'])
def add_category():
    new_category_data = request.get_json()
    new_category = Category(
        name = new_category_data['name']
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message':'Category added succesfully!', 'category':new_category.to_dict()}),201

#update a category (PUT)
@app.route('/category/<int:id>',methods=['PUT'])
def update_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'error':'Category not found'}),404
    updated_data = request.get_json()
    category.name = updated_data.get('name',category.name)
    db.session.commit()
    return jsonify({'message':'Category updated succesfully!' , 'category':category.to_dict()})

#delete a category (DELETE)
@app.route('/category/<int:id>',methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category not found'}),404
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message':'Category deleted successfully!'})

#LEVEL ROUTE==========================================================================>

#get all level
@app.route('/level',methods=['GET'])
def get_levels():
    levels= Level.query.all()
    return jsonify([level.to_dict() for level in levels])

#get level by id
@app.route('/level/<int:id>',methods=['GET'])
def get_level(id):
    level = Level.query.get(id)
    if not level:
        return jsonify({'error':'Level not found'}),404
    return jsonify(level.to_dict())

#new level
@app.route('/level',methods=['POST'])
def add_level():
    new_level_data = request.get_json()
    new_level = Level(
        name = new_level_data['name']
    )
    db.session.add(new_level)
    db.session.commit()
    return jsonify({'message':'Level added succesfully!' ,'level':new_level.to_dict()}),201

#update level (PUT)
@app.route('/level/<int:id>',methods=['PUT'])
def update_level(id):
    level = Level.query.get(id)
    if not level:
        return jsonify({'error':'Level not found'}),404
    
    update_data = request.get_json()
    level.name = update_data.get('name',level.name)
    db.session.commit()
    return jsonify({'message':'Level update successfully!','level':level.to_dict()})

#delete level
@app.route('/level/<int:id>',methods=['DELETE'])
def delete_level(id):
    level = Level.query.get(id)
    if not level:
        return jsonify({'error':'Level not found'}),404
    db.session.delete(level)
    db.session.commit()
    return jsonify({'message':'Level deleted successfullt!'})
    


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error' : 'Not Found'}),404

if __name__ == '__main__':
    app.run(debug=True , port=5000)
