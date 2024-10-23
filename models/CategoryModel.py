from config import db 

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False,unique=True)
    
    books = db.relationship('Book',backref='category',lazy=True)
    
    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name
        }