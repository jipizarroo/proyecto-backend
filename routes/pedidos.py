from flask import Blueprint, request, jsonify
from models import db, Pedido, Info_Pedidos
from flask_jwt_extended import (
    jwt_required
)

route_pedidos = Blueprint('route_pedidos', __name__)

@route_pedidos.route('/pedidos', methods = ['GET'])
@jwt_required
def pedidos_get():
    pedidos = Pedido.query.all()
    pedidos = list(map(lambda pedidos: pedidos.serialize(), pedidos))
    return jsonify(pedidos), 200


@route_pedidos.route('/pedidos', methods = ['POST'])
@jwt_required
def pedidos_post():

    info_pedidos = Info_Pedidos()
    info_pedidos.id_mesa = request.json.get('id_mesa')
    info_pedidos.id_user = 2

    db.session.add(info_pedidos)
    db.session.commit()

    pedidos = request.json.get('productos')
    for p in pedidos:
        pedido = Pedido()
        pedido.id_info_pedidos = info_pedidos.id
        pedido.id_item = 1
        pedido.id_item = p['id_producto']
        pedido.cantidad = p['cantidad']
        db.session.add(pedido)
        db.session.commit()

    return jsonify(info_pedidos.id), 201

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
