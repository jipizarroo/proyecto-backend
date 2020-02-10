from flask import Blueprint, request, jsonify 
from flask_jwt_extended import (
    jwt_required
)
from models import db, Mesa, Plaza

route_filtros = Blueprint('route_filtros', __name__)

@route_filtros.route('/filtros/', methods=['GET'])
@route_filtros.route('/filtros/<int:plaza_id>', methods=['GET'])
@jwt_required


def filtros(plaza_id = None):
    if request.method == 'GET':
        if plaza_id is not None:
            mesas = Mesa.query.filter_by(plaza_id=plaza_id).all()
            mesas = list(map(lambda mesa: mesa.serialize(), mesas))
            return jsonify(mesas), 200
  