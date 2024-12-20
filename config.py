from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS

#init db connect
app = Flask(__name__)
CORS(app,resources={r"/api/*": {"origins": "*"}},supports_credentials=True)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flaskapiPractices_foreigndug:f160a689adba286f94b25abbc358ab59ac99f42b@junbl.h.filess.io:3305/flaskapiPractices_foreigndug'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://pwl123:2wsx1qaz@localhost:3306/db_repository_0627'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '2wsx1qaz'

db = SQLAlchemy(app)

@app.route('/')
def home():
    return "hello world!!!"
app.app_context().push()