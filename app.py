from config import app, db
from routes.Book_bp import book_bp
from routes.Category_bp import category_bp

app.register_blueprint(book_bp)
app.register_blueprint(category_bp)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

# from flask import Flask , jsonify , request
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://pwl123:2wsx1qaz@localhost:3306/db_repository_0627'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# #model book menggunakan sqlalchemy orm
# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     author = db.Column(db.String(100), nullable=False)
#     year = db.Column(db.Integer, nullable=False)
#     description = db.Column(db.String(255),nullable=True)
#     category_id = db.Column(db.Integer , db.ForeignKey('category.id'),nullable=False)
    
#     def to_dict(self):
#         return {
#             'id':self.id,
#             'title':self.title,
#             'author':self.author,
#             'year':self.year,
#             'description':self.description,
#             'category_id':self.category_id
#         }

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), nullable=False, unique=True)
#     password = db.Column(db.String(100), nullable =False)
#     fullname = db.Column(db.String(100), nullable =False)
#     status = db.Column(db.String(100) , nullable =False)
#     level_id = db.Column(db.Integer ,db.ForeignKey('level.id'), nullable =False)
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'username': self.username,
#             'fullname': self.fullname,
#             'password' : self.password,
#             'status': self.status,
#             'level_id': self.level_id
#         }

# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False,unique=True)
    
#     books = db.relationship('Book',backref='category',lazy=True)
    
#     def to_dict(self):
#         return{
#             'id':self.id,
#             'name':self.name
#         }
        
# class Level(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False,unique=True)
    
#     users = db.relationship('User',backref='level',lazy=True)
    
#     def to_dict(self):
#         return{
#             'id':self.id,
#             'name':self.name
#         }

# #init database
# @app.before_request
# def create_tables():
#     app.before_request_funcs[None].remove(create_tables)
#     db.create_all()

# #USER ROUTE==========================================================================>

# #get all user
# @app.route('/users',methods=['GET'])
# def get_users():
#     users = User.query.all()
#     users_with_level =[]
#     for user in users:
#         #get level
#         level = Level.query.get(user.level_id)
#         #add details
#         users_with_level.append({
#             'id': user.id,
#             'username': user.username,
#             'fullname': user.fullname,
#             'password' : user.password,
#             'status': user.status,
#             'level_name': level.name if level else "No Level"
#         })
        
#     response ={
#         'status':'success',
#         'data':{
#             'users':users_with_level
#         },
#         'message':'Users retrived successfully!'
#     }
#     return jsonify(response),200

# #get by id
# @app.route('/users/<int:user_id>',methods=['GET'])
# def get_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'error' : 'user not found'}),404
    
#     #get level
#     level = Level.query.get(user.level_id)
#     user_data = {
#         'id': user.id,
#         'username': user.username,
#         'fullname': user.fullname,
#         'password' : user.password,
#         'status': user.status,
#         'level_name': level.name if level else "No Level"
#     }
    
#     response ={
#         'status':'success',
#         'data':{
#             'user':user_data
#         },
#         'message':'User retrieved successfuly!'
#     }
#     return jsonify(response),200

# #add new user
# @app.route('/users',methods=['POST'])
# def add_user():
#     new_user_data = request.get_json()
#     new_user = User(
#         username = new_user_data['username'],
#         password = new_user_data['password'],
#         fullname = new_user_data['fullname'],
#         status = new_user_data['status'],
#         level_id = new_user_data['level_id']
#     )
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message' : 'user added successfully!','user':new_user.to_dict()}),201

# #update user
# @app.route('/users/<int:user_id>',methods=['PUT'])
# def update_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'error':'user not found'}),404
#     update_data = request.get_json()
#     user.username = update_data.get('username',user.username)
#     user.password = update_data.get('password',user.password)
#     user.fullname = update_data.get('fullname',user.fullname)
#     user.status = update_data.get('status',user.status)
#     user.level_id = update_data.get('level_id',user.level_id)
    
#     db.session.commit()
#     return jsonify({'message' : 'user update successfully!','user' :user.to_dict()})

# #partially update a user (patch)
# @app.route('/users/<int:user_id>', methods=['PATCH'])
# def patch_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'error' : 'user not fount'}),404

#     patch_data = request.get_json()
#     if 'username' in patch_data:
#         user.usename = patch_data['username']
        
#     if 'password' in patch_data:
#         user.password = patch_data['password']
        
#     if 'fullname' in patch_data:
#         user.fullname = patch_data['fullname']
        
#     if 'status' in patch_data:
#         user.status = patch_data['status']
#     if 'level' in patch_data:
#         level = Level.query.get(patch_data['level_id'])
#         if level:
#             user.level_id = patch_data['level_id']
#         else:
#             return jsonify({'error': 'Level not found'}),404
        
#     db.session.commit()
#     return jsonify({'message':'user partially updated successfully!','user':user.to_dict()})

# #delete user
# @app.route('/users/<int:user_id>',methods=['DELETE'])
# def delete_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'error' : 'user not fount'}),404
    
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({'message':'user deleted successfully!'})

# #LEVEL ROUTE==========================================================================>

# #get all level
# @app.route('/level',methods=['GET'])
# def get_levels():
#     levels= Level.query.all()
#     return jsonify([level.to_dict() for level in levels])

# #get level by id
# @app.route('/level/<int:id>',methods=['GET'])
# def get_level(id):
#     level = Level.query.get(id)
#     if not level:
#         return jsonify({'error':'Level not found'}),404
#     return jsonify(level.to_dict())

# #new level
# @app.route('/level',methods=['POST'])
# def add_level():
#     new_level_data = request.get_json()
#     new_level = Level(
#         name = new_level_data['name']
#     )
#     db.session.add(new_level)
#     db.session.commit()
#     return jsonify({'message':'Level added succesfully!' ,'level':new_level.to_dict()}),201

# #update level (PUT)
# @app.route('/level/<int:id>',methods=['PUT'])
# def update_level(id):
#     level = Level.query.get(id)
#     if not level:
#         return jsonify({'error':'Level not found'}),404
    
#     update_data = request.get_json()
#     level.name = update_data.get('name',level.name)
#     db.session.commit()
#     return jsonify({'message':'Level update successfully!','level':level.to_dict()})

# #delete level
# @app.route('/level/<int:id>',methods=['DELETE'])
# def delete_level(id):
#     level = Level.query.get(id)
#     if not level:
#         return jsonify({'error':'Level not found'}),404
#     db.session.delete(level)
#     db.session.commit()
#     return jsonify({'message':'Level deleted successfullt!'})
    


# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({'error' : 'Not Found'}),404

# if __name__ == '__main__':
#     app.run(debug=True , port=5000)
