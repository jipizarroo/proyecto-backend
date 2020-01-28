from flask import Blueprint, request, jsonify 
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    jwt_required
)
from models import db, User

bcrypt = Bcrypt()
route_users = Blueprint('route_users', __name__)

@route_users.route('/users', methods=['GET', 'POST'])
@route_users.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
#@jwt_required

def users(id=None):
    if request.method == 'GET':
        if id is not None:
            user = User.query.get(id)
            if user:
                return jsonify(user.serialize()), 200
            else:
                return jsonify({'user': 'not founf'}), 400
        else:
            users = User.query.all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200
    
    if request.method == 'POST':


        password = request.json.get('password')
        user = User()
        user.name = request.json.get('name')
        user.last_name = request.json.get('last_name')
        user.email = request.json.get('email')
        user.password = bcrypt.generate_password_hash(password)

        if not password:
            return jsonify({"password": "password is required"}), 422
        if not user.name:
            return jsonify({"name": "name is required"}), 422
        if not user.last_name:
            return jsonify({"last_name": "last_name is required"}), 422
        if not user.email:
            return jsonify({"email": "email is required"}), 422

        db.session.add(user)
        db.session.commit()

        #FALTA ENVIAR EMAIL DE CONFORMACIon#
        return jsonify(user.serialize()), 201

    if request.method == 'PUT':

        password = request.json.get('password')
        user = User.query.get(id)
        user.name = request.json.get('name')
        user.last_name = request.json.get('last_name')
        user.email = request.json.get('email')
        user.password = bcrypt.generate_password_hash(password)

        if not password:
            return jsonify({"password": "password is required"}), 422
        if not user.name:
            return jsonify({"name": "name is required"}), 422
        if not user.last_name:
            return jsonify({"last_name": "last_name is required"}), 422
        if not user.email:
            return jsonify({"email": "email is required"}), 422

        db.session.commit()

        return jsonify(user.serialize()), 201        

    if request.method == 'DELETE':
        user= User.query.get(id)
        db.session.delete(user)
        db.session.commit()

        return jsonify({'user': 'deleted'}), 200

        