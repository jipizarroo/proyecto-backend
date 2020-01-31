from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return '<User %r>' % self.name
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'last_name': self.last_name,
        }

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(150), nullable = False)

    def _repr_(self):
        return '<Category %r>' % self.id

    def serialize(self):
        return{
            'id': self.id,
            'description': self.description,
        }

class Item(db.Model):
     __tablename__ = 'items'
     id = db.Column(db.Integer, primary_key = True)
     nombre = db.Column(db.String(150), nullable = False)
     precio = db.Column(db.String(10), nullable = False)
     descripcion = db.Column(db.String(250), nullable = False)

     category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
     category = db.relationship(Category)

     def _repr_(self):
         return '<Item %r>' % self.id

     def serialize(self):
         return{
             'id': self.id,
             'nombre': self.nombre,
             'precio': self.precio,
             'descripcion': self.descripcion,
             'category_id': self.category_id,
             'category': self.category.serialize()
         }