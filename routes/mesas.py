from flask import Blueprint, request, jsonify 
from flask_jwt_extended import (
    jwt_required
)
from models import db, Mesa, Plaza

route_mesas = Blueprint('route_mesas', __name__)

@route_mesas.route('/mesas', methods=['GET', 'POST'])
@route_mesas.route('/mesas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required

def mesas(id = None):
    if request.method == 'GET':
        if id is not None:
            mesa = Mesa.query.get(id)
            if mesa:
                return jsonify(mesa.serialize()), 200
            else:
                return jsonify({'msg': 'Mesa not found'}), 404
        else:
             mesas = Mesa.query.all()
             mesas = list(map(lambda mesa: mesa.serialize(), mesas))
             return jsonify(mesas), 200

    if request.method == 'POST':
        cantidad_mesa = int(request.json.get('cantidad_mesa'))
        plaza_id = request.json.get('plaza_id')

        if not cantidad_mesa:
            return jsonify({"msg": "cantidad mesa: is required"}), 422
        if not plaza_id:
            return jsonify({"msg": "Seleccionar plaza: is required"}), 422

        plaza = Plaza.query.get(plaza_id)

        if not plaza:
            return jsonify({"msg": "Plaza doesn't exists"}), 404

        mesas = Mesa.query.all()
        mesas = Mesa.query.filter_by(plaza_id=plaza_id).all()
        mesas = list(map(lambda mesa: mesa.serialize(), mesas))
        if (len(mesas) == 0) and (int(cantidad_mesa) > 1):
            for i in range(cantidad_mesa):
                mesa = Mesa()
                mesa.plaza_id = request.json.get('plaza_id')
                mesa.nombre_mesa = plaza.nombre_plaza + str(i+1)

                db.session.add(mesa)
                db.session.commit()

            return jsonify({"msg": "Mesas han sigo agregadas"}),201

        elif (len(mesas) > 0) and (int(cantidad_mesa) > 1):
            for i in range(cantidad_mesa):
                mesa=Mesa()
                mesa.plaza_id = request.json.get('plaza_id')
                mesa.nombre_mesa = plaza.nombre_plaza + str(i+(len(mesas))+1)

                db.session.add(mesa)
                db.session.commit()
            return jsonify({"msg": "Mesas han sido agregadas"}),201

        elif (len(mesas) > 0) and (int(cantidad_mesa) == 1):
            mesa=Mesa()
            mesa.plaza_id = request.json.get('plaza_id')
            mesa.nombre_mesa = plaza.nombre_plaza + str(1+len(mesas))

            db.session.add(mesa)
            db.session.commit()
            return jsonify(mesa.serialize()), 201

        elif (len(mesas) == 0) and (int(cantidad_mesa) == 1):
            mesa=Mesa()
            mesa.plaza_id = request.json.get('plaza_id')
            mesa.nombre_mesa = plaza.nombre_plaza + str(1)

            db.session.add(mesa)
            db.session.commit()
            return jsonify(mesa.serialize()),201
            
    
    if request.method == 'PUT':

        mesa = Mesa.query.get(id)
        mesa.nombre_mesa = request.json.get('nombre_mesa')

        if not mesa.nombre_mesa:
            return jsonify({"msg": "ID Mesa is required"}), 422


        db.session.commit()

        return jsonify(mesa.serialize()), 201

    if request.method == 'DELETE':

        mesa = Mesa.query.get(id)
        db.session.delete(mesa)
        db.session.commit()

        return jsonify({'msg': 'mesa deleted'}), 201   