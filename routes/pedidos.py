from flask import Blueprint, request, jsonify
from models import db, Pedido, Info_Pedidos, User
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
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

    #Obtencion de id dede el token!!!!!
    user_email =  get_jwt_identity()
    user = User.query.filter_by(email = user_email).first()

    if user:
        info_pedidos = Info_Pedidos()
        info_pedidos.id_mesa = request.json.get('id_mesa')
        info_pedidos.id_user = user.id

        db.session.add(info_pedidos)
        db.session.commit()

        pedidos = request.json.get('productos')
        for p in pedidos:
            pedido = Pedido()
            pedido.id_info_pedidos = info_pedidos.id
            pedido.id_item = p['id_producto']
            pedido.cantidad = p['cantidad']
            db.session.add(pedido)
            db.session.commit()

        info_resumen = Info_Pedidos.query.get(info_pedidos.id)
        pedidos = Pedido.query.filter_by(id_info_pedidos = info_resumen.id).all()
        info_total = {}
        info_total["info_pedido"] = info_resumen.serialize()
        info_total["pedidos"] = [pedido.serialize() for pedido in pedidos]
        info_total["total"] = 0 if len(pedidos) == 0 else sum(float(pedido.cantidad) * float(pedido.item.precio)  for pedido in pedidos)
        return jsonify(info_total), 201
    
    return "Usuario no encontrado", 404
