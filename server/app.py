from flask import Flask, jsonify, request, redirect, g, make_response
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin
from flask_restful import Api
from flask_jwt_extended import JWTManager


# DATABASE RELATED IMPORTS
from server.db_models.db import db
from server.db_models.defaults import default_blueprint_shield, default_blueprint_weapon

from server.db_models.Blueprint import Blueprint
from server.db_models.Character import Character
from server.db_models.Enemy import Enemy
from server.db_models.ItemsInGame import ItemsInGame
from server.db_models.NonPersonCharacter import NonPersonCharacter
from server.db_models.RevokedTokenModel import RevokedTokenModel
# from server.db_models.User import User

# from server.func_resources import *
import server.resources as resources


login_site_path = 'front/main_page/index.html'

app = Flask(__name__)
api = Api(app)
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://game_admin:#dmiN123@localhost/game'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

auth = HTTPBasicAuth()


@jwt.token_in_blacklist_loader
def check_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_blacklisted(jti)


@app.before_first_request
def manage_db():
    db.init_app(app)
    db.drop_all(app=app)
    db.create_all(app=app)
    default_blueprint_weapon.save()
    default_blueprint_shield.save()


api.add_resource(resources.UserRegistration, '/r')
api.add_resource(resources.UserLogin, '/l')
api.add_resource(resources.CharacterFight, '/fight')
if __name__ == '__main__':
    app.run()
