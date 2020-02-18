from flask import Blueprint, request, jsonify 
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from models import db, User
import datetime
from libs.functions import sendMail

bcrypt = Bcrypt()
route_first_user = Blueprint('route_first_user', __name__)

@route_first_user.route('/first_user', methods=['GET', 'POST'])
def first_user():
    if request.method == 'GET':
        user = User.query.all()
        user = list(map(lambda user:user.serialize(), user))
        return jsonify(user), 200
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

        users = User.query.all()
        if not users: 
            user = User()
            user.name = name
            user.last_name = last_name
            user.email = email
            user.password = bcrypt.generate_password_hash(password)
            user.isAdmin = True

            db.session.add(user)
            db.session.commit()

            sendMail("Usuario Creado", user.email, "jipizarroo@gmail.com", user.email, "Bienvenido "+user.name+user.last_name+ " recuerda siempre dejar un admin, de borrar todo los admin debes contactarnos :)!")

            if bcrypt.check_password_hash(user.password, password):
                #expires = datetime.timedelta(days=3)
                access_token = create_access_token(identity=user.email, expires_delta=False)
                data = {
                    "access_token": access_token,
                    "user": user.serialize()
                }
                return jsonify(data), 200

            return jsonify(user.serialize()), 201

        else:
            return jsonify({"msg": "Can only create one admin with this method"}), 404