from flask import Blueprint, request, jsonify 
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from models import db, User
import datetime

from libs.functions import sendMail

bcrypt = Bcrypt()
route_users = Blueprint('route_users', __name__)

@route_users.route('/users', methods=['GET', 'POST'])
@route_users.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required

def users(id=None):
    if request.method == 'GET':
        if id is not None:
            user = User.query.get(id)
            if user:
                return jsonify(user.serialize()), 200
            else:
                return jsonify({'user': 'not found'}), 400
        else:
            users = User.query.all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200
    
    if request.method == 'POST':

        password = request.json.get('password')
        name = request.json.get('name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')

        if not password:
            return jsonify({"msg": "password is required"}), 422
        if not name:
            return jsonify({"msg": "name is required"}), 422
        if not last_name:
            return jsonify({"msg": "last_name is required"}), 422
        if not email:
            return jsonify({"msg": "email is required"}), 422

        username = User.query.filter_by(email=email).first()

        if username:
            return jsonify({"msg": "Email is taken"}), 404


        user = User()
        user.name = name
        user.last_name = last_name
        user.email = email
        user.password = bcrypt.generate_password_hash(password)


        db.session.add(user)
        db.session.commit()

        sendMail("Usuario Creado", user.email, "jipizarroo@gmail.com", user.email, "Bienvenido "+user.name+user.last_name+ " recuerda tu usuario es tu mismo email!")

        if bcrypt.check_password_hash(user.password, password):
            #expires = datetime.timedelta(days=3)
            access_token = create_access_token(identity=user.email, expires_delta=False)
            data = {
                "access_token": access_token,
                "user": user.serialize()
            }
            return jsonify(data), 200

        #FALTA ENVIAR EMAIL DE CONFORMACIon#
        return jsonify(user.serialize()), 201

    if request.method == 'PUT':

        #password = request.json.get('password')
        user = User.query.get(id)
        user.name = request.json.get('name')
        user.last_name = request.json.get('last_name')
        user.email = request.json.get('email')
        user.isAdmin = request.json.get('isAdmin')
        user.isActive = request.json.get('isActive')
        #user.password = bcrypt.generate_password_hash(password)

        #if not password:
            #return jsonify({"msg": "password is required"}), 422
        if not user.name:
            return jsonify({"msg": "name is required"}), 422
        if not user.last_name:
            return jsonify({"msg": "last_name is required"}), 422
        if not user.email:
            return jsonify({"msg": "email is required"}), 422

        db.session.commit()

        sendMail("Usuario Creado", user.email, "jipizarroo@gmail.com", user.email, "Modificaciones aplicadas "+user.name+user.last_name)

        return jsonify(user.serialize()), 201        

    if request.method == 'DELETE':
        user= User.query.get(id)
        db.session.delete(user)
        db.session.commit()

        return jsonify({'user': 'deleted'}), 200

        