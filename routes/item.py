from flask import Blueprint, request, jsonify
from models import db, Item

route_items = Blueprint('route_items', __name__)

@route_items.route('/items', methods = ['GET', 'POST'])
@route_items.route('/items/<int:id>', methods = ['GET', 'PUT', 'DELETE'])

def items(id = None):
    if request.method == 'GET':
        if id is not None:
            item = Item.query.get(id)
            if item:
                return jsonify(item.serialize()), 200
            else:
                return jsonify({'item': 'not found'}), 404
        else:
            items = Item.query.all()
            items = list(map(lambda item: item.serialize(), items))
            return jsonify(items), 200
    
    if request.method == 'POST':
    
        # validar el request

        item = Item()
        item.nombre = request.json.get('nombre')
        item.precio = request.json.get('precio')
        item.descripcion = request.json.get('descripcion')

        db.session.add(item)
        db.session.commit()

        return jsonify(item.serialize()), 201 

    if request.method == 'PUT':
        
        # validar el request

        item = Item.query.get(id)
        item.nombre = request.json.get('nombre')
        item.precio = request.json.get('precio')
        item.descripcion = request.json.get('descripcion')

        db.session.commit()

        return jsonify(item.serialize()), 200

    if request.method == 'DELETE':
        
        item = Item.query.get(id)
        db.session.delete(item)
        db.session.commit()

        return jsonify({'item': 'deleted'}), 200