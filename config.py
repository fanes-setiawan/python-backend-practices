from flask_sqlalchemy import SQLAlchemy
from flask import Flask

#init db connect
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flaskapiPractices_foreigndug:f160a689adba286f94b25abbc358ab59ac99f42b@junbl.h.filess.io:3305/flaskapiPractices_foreigndug'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def home():
    return "hello world!!!"
app.app_context().push()