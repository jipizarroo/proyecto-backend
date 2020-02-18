from flask import Blueprint, request, jsonify
from models import db, Item
from flask_jwt_extended import (
    jwt_required
)

route_items = Blueprint('route_items', __name__)


@route_items.route('/items', methods=['GET', 'POST'])
@route_items.route('/items/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def items(id=None):
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
        if not request.json.get('nombre'):
            return jsonify({"nombre": "is required"}), 422
        if not request.json.get('precio'):
            return jsonify({"precio": "is required"}), 422
        if not request.json.get('descripcion'):
            return jsonify({"descripcion": "is required"}), 422
        if not request.json.get('category_id'):
            return jsonify({"category_id": "is required"}), 422

        item = Item()
        item.nombre = request.json.get('nombre')
        item.precio = request.json.get('precio')
        item.descripcion = request.json.get('descripcion')
        item.category_id = request.json.get('category_id')

        db.session.add(item)
        db.session.commit()

        return jsonify(item.serialize()), 201

    if request.method == 'PUT':
        if not request.json.get('nombre'):
            return jsonify({"nombre": "is required"}), 422
        if not request.json.get('precio'):
            return jsonify({"precio": "is required"}), 422
        if not request.json.get('descripcion'):
            return jsonify({"descripcion": "is required"}), 422
        if not request.json.get('category_id'):
            return jsonify({"category_id": "is required"}), 422

        item = Item.query.get(id)
        item.nombre = request.json.get('nombre')
        item.precio = request.json.get('precio')
        item.descripcion = request.json.get('descripcion')
        item.category_id = request.json.get('category_id')

        db.session.commit()

        return jsonify(item.serialize()), 200

    if request.method == 'DELETE':

        item = Item.query.get(id)
        db.session.delete(item)
        db.session.commit()

        return jsonify({'item': 'deleted'}), 200
