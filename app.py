import os
from flask import Flask, render_template, jsonify, request, Blueprint
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_jwt_extended import (
    JWTManager
)
from models import db, User, Item, Category, Plaza, Mesa, Pedido
from routes.user import route_users
from routes.category import route_categories
from routes.item import route_items
from routes.plazas import route_plazas
from routes.mesas import route_mesas
from routes.pedidos import route_pedidos
from routes.filtrar import route_filtros
from routes.auth import auth
from routes.first_user import route_first_user
from routes.info_pedidos import route_info_pedidos

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/img')
# ALLOWED_EXTENSION = {'jpg', 'png', 'jpeg'}
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True  #SE PONE FALSO CUANDO SE SUBE A PRODUCCION
app.config['ENV'] = 'development'    

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'jipizarroo@gmail.com'
app.config['MAIL_PASSWORD'] = 'nfjjobyrbqaeqmzx'

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['JWT_SECRET_KEY'] = 'super-secret' #Change this when on production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = True
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=3)

jwt = JWTManager(app)
db.init_app(app)
mail = Mail(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
CORS(app)

@app.route('/')
def home(): 
    return render_template('index.html', name="home")

app.register_blueprint(auth)
app.register_blueprint(route_users, url_prefix='/api')
app.register_blueprint(route_categories, url_prefix='/api')
app.register_blueprint(route_items, url_prefix='/api')
app.register_blueprint(route_plazas, url_prefix='/api')
app.register_blueprint(route_mesas, url_prefix='/api')
app.register_blueprint(route_pedidos, url_prefix='/api')
app.register_blueprint(route_filtros, url_prefix='/api')
app.register_blueprint(route_first_user, url_prefix='/api')
app.register_blueprint(route_info_pedidos, url_prefix='/api')


if __name__ == "__main__":
    manager.run()