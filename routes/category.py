from flask import Blueprint, request, jsonify
from models import db, Category, Item
from flask_jwt_extended import (
    jwt_required
)

route_categories = Blueprint('route_categories', __name__)

@route_categories.route('/categories', methods = ['GET'])
@jwt_required
def categories_get():
    categories = Category.query.all()
    categories = list(map(lambda category: category.serialize(), categories))
    return jsonify(categories), 200


@route_categories.route('/categories', methods = ['POST'])
@jwt_required
def categories_post():

    category = Category()
    category.description = request.json.get('description')

    db.session.add(category)
    db.session.commit()

    return jsonify(category.serialize()), 201


@route_categories.route('/categories/<int:id>', methods = ['GET'])
@jwt_required
def categories_id_get(id = None):
    items = Item.query.filter_by(category_id = id).all()
    result = [x.serialize() for x in items]
    return jsonify(result), 200


@route_categories.route('/categories/<int:id>', methods = ['PUT'])
@jwt_required
def categories_id_put(id = None):

    category = Category.query.get(id)
    category.description = request.json.get('description')

    db.session.commit()

    return jsonify(category.serialize()), 200


@route_categories.route('/categories/<int:id>', methods = ['DELETE'])
@jwt_required
def categories_id_delete(id = None):
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()

    return jsonify({'category': 'deleted'}), 200
