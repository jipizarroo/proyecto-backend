from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, get_jwt_identity
)
from flask_bcrypt import Bcrypt
from models import db, User
import datetime

bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email:
        return jsonify({"msg": "Email es requerido"}), 422
    if not password:
        return jsonify({"msg": "Password es requerida"}), 422

    user = User.query.filter_by(email=email).first()

    if not user: 
        return jsonify ({"msg": "email not found"}), 404
    pw_hash = bcrypt.generate_password_hash(password)
    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.email, expires_delta=False)
        data = {
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 200
    else:
        return jsonify({"msg": "email/password is wrong"}), 401
