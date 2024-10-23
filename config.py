from flask_sqlalchemy import SQLAlchemy
from flask import Flask

#init db connect
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://pwl123:2wsx1qaz@localhost:3306/db_repository_0627'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()