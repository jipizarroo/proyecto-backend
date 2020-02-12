from flask import Blueprint, request, jsonify 
from flask_jwt_extended import (
    jwt_required
)
from models import db, Info_Pedidos, Pedido

route_info_pedidos = Blueprint('route_info_pedidos', __name__)


#@jwt_required

@route_info_pedidos.route('/info-pedidos', methods=['GET'])
def info_pedido():
    #Obtencion de id dede el token!!!!!
    id_user = 2
    #---------------------------------

    infos = Info_Pedidos.query.filter_by(id_user = id_user).all()
    infos = [info.serialize() for info in infos]

    return jsonify(infos), 200

@route_info_pedidos.route('/info-pedidos/<int:id>', methods=['GET'])
def info_pedido_id(id):
    info = Info_Pedidos.query.get(id)

    if info:
        pedidos = Pedido.query.filter_by(id_info_pedidos = info.id)
        info_total = {}
        info_total["info_pedido"] = info.serialize()
        info_total["pedidos"] = [pedido.serialize() for pedido in pedidos]
        return jsonify(info_total), 200
    else:
        return jsonify({'msg': 'Informacion de pedido not found'}), 404