from config import db 

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