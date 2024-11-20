from config import app, db
from routes.Book_bp import book_bp
from routes.Category_bp import category_bp
from routes.User_bp import user_bp
from routes.Level_bp import level_bp
from flask import request,jsonify
from controllers.UserController import check_password_hash
from models.UserModel import User

app.register_blueprint(book_bp)
app.register_blueprint(category_bp)
app.register_blueprint(user_bp)
app.register_blueprint(level_bp)

@app.before_request
def before_request():
    print("Before Request")
    excluded_routes = ['/api/login','/api/register','/api/users']
    if request.path in excluded_routes:
        return None
    #auth all routes
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message':'Authentication Failed'}),401
    #cek user to database
    user = User.query.filter_by(username=auth.username).first()
    if not user or not check_password_hash(user.password,auth.password):
        return jsonify({'message':'Invalid username or password'}),401
    
    request.current_user = user



db.create_all()
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
