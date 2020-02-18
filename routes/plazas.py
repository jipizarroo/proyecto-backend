from flask import Blueprint, request, jsonify 
from flask_jwt_extended import (
    jwt_required
)
from models import db, Plaza

route_plazas = Blueprint('route_plazas', __name__)

@route_plazas.route('/plazas', methods=['GET', 'POST'])
@route_plazas.route('/plazas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required

def plazas (id=None):
    if request.method == 'GET':
        if id is not None:
            plaza = Plaza.query.get(id)
            if user:
                return jsonify(plaza.serialize()),200
            else:
                return jsonify({'msg': 'Plaza is not found'}), 400
        else:
            plazas = Plaza.query.all()
            plazas = list(map(lambda plaza: plaza.serialize(), plazas))
            return jsonify(plazas), 200
    
    if request.method == 'POST':

        plaza = Plaza()
        plaza.nombre_plaza = request.json.get('nombre_plaza')

        if not plaza.nombre_plaza:
            return jsonify({"msg": "Nombre plaza is required"}), 422
        
        
        db.session.add(plaza)
        db.session.commit()

        return jsonify(plaza.serialize()), 201
    
    if request.method == 'PUT':

        plaza = Plaza.query.get(id)
        plaza.nombre_plaza = request.json.get('nombre_plaza')

        if not plaza.nombre_plaza:
            return jsonify({"msg": "plaza id is required"}), 422            
        
        db.session.commit()

        return jsonify(plaza.serialize()), 201

    if request.method == 'DELETE':
        plaza = Plaza.query.get(id)
        db.session.delete(plaza)
        db.session.commit()

        return jsonify({'msg': 'Plaza deleted'}), 200



