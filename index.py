from config import app, db
from routes.Book_bp import book_bp
from routes.Category_bp import category_bp
from routes.User_bp import user_bp
from routes.Level_bp import level_bp
from flask import request,jsonify
from models.UserModel import User
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required

app.register_blueprint(book_bp)
app.register_blueprint(category_bp)
app.register_blueprint(user_bp)
app.register_blueprint(level_bp)

jwt = JWTManager(app)

@app.before_request
def before_request():
    print("Before Request")
    excluded_routes = ['/api/login','/api/register']
    if request.path in excluded_routes:
        return None
    
@app.route('/api/protected',methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user),200



db.create_all()
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
