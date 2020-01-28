from flask import Blueprint, request, jsonify 
from models import db, Producto


route_productos = Blueprint('route_productos', __name__)


@route_productos.route('/data_productos', methods=['GET','POST'])
@route_productos.route('/data_productos/<int:id>', methodos=['GET', 'PUT', 'DELETE'])
#@jwt_required
def tipo_producto(id=None):
    if request.method == 'GET':
        if id is not None:
            producto = Producto.query.get(id)
            if producto:
                return jsonify(producto.serialize()), 200
            else:
                return({"producto": "Not Found"}),404
        else:
            producto = Producto.query.all()
            producto = list(map(lambda producto: producto.serialize(), producto))
            return jsonify(producto)
    
    if request.method == 'POST':
        
        producto = Producto()
        producto.nombre = request.json.get("nombre")
        producto.precio =  request.json.get("precio")

        db.session.add(producto)
        db.session.commit()

        return jsonify(producto.serialize()), 201
    
    if request.method == 'PUT':
        
        producto = Producto.query.get(id)
        producto.nombre = request.json.get("nombre")
        producto.precio =  request.json.get("precio")
        
        db.session.commit()
        return jsonify(producto.serialize()),200

    if request.method == 'DELETE':
        producto = Producto.query.get(id)
        db.session.delete(producto)
        db.session.commit()

        return jsonify({"producto": "deleted"}), 200
