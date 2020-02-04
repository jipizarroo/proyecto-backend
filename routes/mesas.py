from flask import Blueprint, request, jsonify 
from flask_jwt_extended import (
    jwt_required
)
from models import db, Mesa

route_mesas = Blueprint('route_mesas', __name__)

@route_mesas.route('/mesas', methods=['GET', 'POST'])
@route_mesas.route('/mesas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
#@jwt_required

def mesas(id = None):
    if request.method == 'GET':
        if id is not None:
            mesa = Mesa.query.get(id)
            if item:
                return jsonify(mesa.serialize()), 200
            else:
                return jsonify({'item': 'not found'}), 404
        else:
             mesas = Mesa.query.all()
             mesas = list(map(lambda mesa: mesa.serialize(), mesas))
             return jsonify(mesas), 200

    if request.method == 'POST':
        cantidad_mesa = int(request.json.get('cantidad_mesa'))
        plaza_id = request.json.get('plaza_id')

        if not numero_mesa:
            return jsonify({"numero de mesas": "is required"}), 422
        if not mesa.plaza_id:
            return jsonify({"id de plaza": "is required"}), 422

        if int(numero_mesa) > 1:
            for i in range(numero_mesa):
                mesa = Mesa()
                mesa.numero_mesa = i + 1

                db.session.add(mesa)
                db.session.commit()

            return jsonify({"msg": "Mesas han sigo agregadas"})

        else:
            mesa = Mesa()
            mesa.plaza_id = request.json.get('plaza_id')

            db.sessions.add(mesa)
            db.session.commit()

            return jsonify(mesa.serialize()), 201
    
    if request.method == 'PUT':

        mesa = Mesa.query.get(id)
        mesa.numero_mesa = request.json.get('numero_mesa')
        mesa.plaza_id = request.json.get('plaza_id')

        if not mesa.numero_mesa:
            return jsonify({"numero de mesas": "is required"}), 422
        if not plaza_id:
            return jsonify({"id de plaza": "is required"}), 422

        db.session.commit()

        return jsonify(plaza.serialize()), 201

    if request.method == 'DELETE':

        mesa = Mesa.query.get(id)
        mesa.numero_mesa = request.json.get('numero_mesa')
        mesa.plaza_id = request.json.get('plaza_id')   

        return jsonify(plaza.serialize()), 201     