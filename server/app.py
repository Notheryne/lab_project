from flask import Flask, jsonify, request, redirect, g, make_response
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin
from flask_restful import Api


# DATABASE RELATED IMPORTS
from server.db_models.extensions import db, jwt
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


def create_app():
    new_app = Flask(__name__)
    new_api = Api(new_app)
    # app.config['SQLALCHEMY_ECHO'] = True
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

    auth = HTTPBasicAuth()

    return new_app, new_api


app, api = create_app()


@app.before_first_request
def manage_db():
    # db.drop_all(app=app)
    db.create_all(app=app)
    healer = NonPersonCharacter(
        name='Akara',
        healer=True,
        trader=False,
        text1="Welcome back, my friend. We are still clearing."
              "the monastery, but you're welcome to stay here as long as you need.",
        text2="Good day. You seem wounded, come and maybe we can fix that.",
        text3="The Order welcomes you. Do you need healing?",
        img_path="https://cdnb.artstation.com/p/assets/images/images/014/413/607/large/greg-mack-akara.jpg?1544499463"
    )
    trader = NonPersonCharacter(
        name='Hephaistos',
        healer=False,
        trader=True,
        text1="Welcome back. Do you need a solid piece of armor?",
        text2="Hi, it's you! I've prepared some special items for my"
              "favourite customer.",
        text3="The Order welcomes you. Your armor seems a little worn out, how about a new one?",
        img_path='http://images6.fanpop.com/image/photos/33400000/Hephaistos-hephaestus-33419337-474-480.jpg'
    )
    # import random
    # i = 0
    # while i < 50:
    #     print(i)
    #     blueprint = Blueprint(**{
    #         'slot': 3,
    #         'name': 'Blueprint helmet #{0}'.format(i),
    #         'price': random.randint(10, 1000),
    #         'max_health': random.randint(0, 50),
    #         'strength': random.randint(0, 20),
    #         'reflex': random.randint(0, 20),
    #         'charisma': random.randint(0, 20),
    #         'intelligence': random.randint(0, 20),
    #         'will': random.randint(0, 20),
    #         'armor': random.randint(0, 20),
    #         'min_dmg': random.randint(0, 20),
    #         'max_dmg': random.randint(20, 40),
    #         'image_path': 'https://gamepedia.cursecdn.com/pathofexile_gamepedia/6/6a/Iron_Hat_inventory_icon.png?version=dd409e0a4ca283e7afbeb5efdf27741e',
    #     })
    #     blueprint.save()
    #     i += 1
    # healer.save()
    # trader.save()
    default_blueprint_weapon.save()
    default_blueprint_shield.save()


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
api.add_resource(resources.AccountManageView, '/api/manage')

api.add_resource(resources.CharacterFight, '/api/arena/fight')
api.add_resource(resources.MonsterFight, '/api/expedition/fight')

api.add_resource(resources.HealerHeal, '/api/npc/heal')
api.add_resource(resources.TraderBuy, '/api/npc/trade')

api.add_resource(resources.AddStat, '/api/add/stats')


api.add_resource(resources.AddItem, '/api/add/item')
api.add_resource(resources.AddBlueprint, '/api/add/blueprint')
api.add_resource(resources.AddEnemy, '/api/add/enemy')


if __name__ == '__main__':
    app.run(debug=True)

# """
# SELECT * FROM items_in_game
# WHERE char_id IN (
#     SELECT id FROM `character`
#     WHERE id IN (
#         SELECT DISTINCT u.id
#         FROM `user` as u
#         INNER JOIN `character` AS c
#         ON c.user_id = u.id
#         INNER JOIN items_in_game AS ig
#         ON ig.char_id = c.id
#         INNER JOIN (
#         SELECT * FROM blueprint
#             WHERE price > 500
#         ) AS expensive_bp
#         ON expensive_bp.id = ig.bp_id
#     )
# );
# """
