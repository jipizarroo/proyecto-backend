from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    isAdmin = db.Column(db.Boolean, default = False, nullable = False)
    isActive = db.Column(db.Boolean, default = True, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.name
    
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'last_name': self.last_name,
            'isAdmin': self.isAdmin,
            'isActive': self.isActive
        }

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(150), nullable = False)

    def __repr__(self):
        return '<Category %r>' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'description': self.description,
        }

class Item(db.Model):
     __tablename__ = 'items'
     id = db.Column(db.Integer, primary_key = True)
     nombre = db.Column(db.String(150), nullable = False)
     precio = db.Column(db.Float, nullable = False)
     descripcion = db.Column(db.String(250), nullable = False)
     category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)

     category = db.relationship(Category)

     def __repr__(self):
         return '<Item %r>' % self.name

     def serialize(self):
         return{
             'id': self.id,
             'nombre': self.nombre,
             'precio': self.precio,
             'descripcion': self.descripcion,
             'category_id': self.category_id,
             'category_descripcion': self.category.description,
         }

class Plaza(db.Model):
    __tablename__ = 'plazas'
    id = db.Column(db.Integer, primary_key = True)
    nombre_plaza = db.Column(db.String(50), nullable = False)

    def __repr__(self):
         return '<Plaza %r>' % self.name

    def serialize(self):
         return{
             'id': self.id,
             'nombre_plaza': self.nombre_plaza,
         }
    

class Mesa(db.Model):
    __tablename__ = 'mesas'
    id = db.Column(db.Integer, primary_key = True)
    nombre_mesa = db.Column(db.String(50), nullable = False)

    plaza_id= db.Column(db.Integer, db.ForeignKey('plazas.id'), nullable = False)
    plaza = db.relationship(Plaza, backref=backref("children", cascade="all,delete"))

    def __repr__(self):
         return '<Mesa %r>' % self.name

    def serialize(self):
         return{
             'id': self.id,
             'nombre_mesa': self.nombre_mesa,
             'plaza': self.plaza.serialize()
             }

# Tabla Pedido
class Info_Pedidos(db.Model):
    __tablename__ = 'info_pedidos'
    id = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    id_mesa = db.Column(db.Integer, db.ForeignKey('mesas.id'), nullable = False)
    abierto = db.Column(db.Boolean, nullable = False, default=True)
    
    user = db.relationship(User, uselist = False)

    def serialize(self):
         return{
             'id': self.id,
             #'id_user': self.id_user,
             'user': self.user.serialize(),
             'id_mesa': self.id_mesa,
         }
    
    def serialize_sin_user(self):
         return{
             'id': self.id,
             'id_user': self.id_user,
             'id_mesa': self.id_mesa,
         }

# Tabla Items de Pedidos
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key = True)
    id_item = db.Column(db.Integer, db.ForeignKey('items.id'), nullable = False)
    id_info_pedidos = db.Column(db.Integer, db.ForeignKey('info_pedidos.id'), nullable = False)
    cantidad = db.Column(db.Integer, nullable = False)
    #fecha_pedido = db.Column(db.Date, nullable = False, default= Date.now())
    

    item = db.relationship(Item)
    info_pedidos = db.relationship(Info_Pedidos)

    def __repr__(self):
         return '<Pedidos %r>' % self.name

    def serialize(self):
         return{
             'item': self.item.serialize(),
             'cantidad': self.cantidad,
         }
