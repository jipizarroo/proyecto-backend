from flask import Blueprint, request, jsonify
from models import db, Item, User, Mesa, Pedido

route_pedidos = Blueprint('route_pedidos', __name__)

@route_pedidos.route('/pedidos', methods = ['GET'])
def pedidos_get():
    pedidos = Pedido.query.all()
    pedidos = list(map(lambda pedidos: pedidos.serialize(), pedidos))
    return jsonify(pedidos), 200


@route_pedidos.route('/pedidos', methods = ['POST'])
def pedidos_post():

    id_mesa = request.json.get('id_mesa')
    pedidos = request.json.get('productos')
    print(id_mesa)
    print(pedidos[0])
    return jsonify(""), 201

    # item_id = request.json.get('item_id')
    # mesa_id = request.json.get('mesa_id')
    # user_id = request.json.get('user_id')

    # pedido = Pedido()
    # pedido.item_id = request.json.get('[item_id]')
    # pedido.mesa_id = request.json.get('mesa_id')
    # pedido.user_id = request.json.get('user_id')

    # db.session.add(pedido)
    # db.session.commit()

    # return jsonify(pedido.serialize()), 201


# @route_categories.route('/categories/<int:id>', methods = ['PUT'])
# def categories_id_put(id = None):
#     # validar el request

#     category = Category.query.get(id)
#     category.description = request.json.get('description')

#     db.session.commit()

#     return jsonify(category.serialize()), 200


# @route_categories.route('/categories/<int:id>', methods = ['DELETE'])
# def categories_id_delete(id = None):
#     category = Category.query.get(id)
#     db.session.delete(category)
#     db.session.commit()

#     return jsonify({'category': 'deleted'}), 200
