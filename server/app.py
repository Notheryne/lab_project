from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_migrate import Migrate

# DATABASE RELATED IMPORTS
from server.db_models.extensions import db, jwt
from server.db_models.defaults import default_blueprints, default_npcs

from server.db_models.Blueprint import Blueprint
from server.db_models.NonPersonCharacter import NonPersonCharacter
from server.db_models.RevokedTokenModel import RevokedTokenModel
from server.db_models.Character import Character
from server.db_models.ItemsInGame import ItemsInGame

from server.db_models.initial_population import populate


import server.resources as resources


def create_app():
    new_app = Flask(__name__)
    new_api = Api(new_app)
    new_app.config['SQLALCHEMY_RECORD_QUERIES'] = True
    new_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:#dmiN123@localhost/game'
    new_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    new_app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    new_app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    new_app.config['JWT_BLACKLIST_ENABLED'] = True

    jwt.init_app(new_app)
    db.init_app(new_app)

    @jwt.token_in_blacklist_loader
    def check_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_blacklisted(jti)

    CORS(new_app)
    new_app.config['CORS_HEADERS'] = 'Content-Type'

    return new_app, new_api


app, api = create_app()
migrate = Migrate(app, db)


@app.before_first_request
def manage_db():
    if DROP:
        db.drop_all(app=app)
    db.create_all(app=app)

    for npc in default_npcs:
        npc_in_db = NonPersonCharacter.find_by_name(npc.name)
        if not npc_in_db:
            npc.save()

    for blueprint in default_blueprints:
        blueprint_in_db = Blueprint.find_by_name(blueprint.name)
        if not blueprint_in_db:
            blueprint.save()

    if POPULATE:
        users = 0
        items = 0
        enemies = 0
        give_items_to = 600
        populate(users, items, enemies, give_items_to)


api.add_resource(resources.UserRegistration, '/api/register')
api.add_resource(resources.UserLogin, '/api/login')
api.add_resource(resources.Refresh, '/api/refresh')

api.add_resource(resources.UserLogout, '/api/logout')
api.add_resource(resources.UserLogoutRefresh, '/api/logout/refresh')

api.add_resource(resources.CharacterView, '/api/character')
api.add_resource(resources.ArenaView, '/api/arena')
api.add_resource(resources.ExpeditionView, '/api/expedition')
api.add_resource(resources.HealerView, '/api/npc/healer')
api.add_resource(resources.TraderView, '/api/npc/trader')
api.add_resource(resources.AccountManageView, '/api/account')

api.add_resource(resources.CharacterFight, '/api/arena/fight')
api.add_resource(resources.MonsterFight, '/api/expedition/fight')

api.add_resource(resources.HealerHeal, '/api/npc/heal')
api.add_resource(resources.TraderBuy, '/api/npc/trade')

api.add_resource(resources.Ranking, '/api/ranking')
api.add_resource(resources.AccountManage, '/api/account/manage')
api.add_resource(resources.AddStat, '/api/add/stats')


api.add_resource(resources.AddItem, '/api/add/item')
api.add_resource(resources.AddBlueprint, '/api/add/blueprint')
api.add_resource(resources.AddEnemy, '/api/add/enemy')

DROP = False
POPULATE = False

if __name__ == '__main__':
    app.run(debug=True)
