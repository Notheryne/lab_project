from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, \
    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt

from server.db_models.User import User
from server.db_models.RevokedTokenModel import RevokedTokenModel
from server.db_models.Character import Character
from server.db_models.Enemy import Enemy
from server.db_models.NonPersonCharacter import NonPersonCharacter

from server.db_models.defaults import create_default_character

from server.func_resources import *

reg_parser = reqparse.RequestParser()
reg_parser.add_argument('username', help='This field cannot be blank', required=True)
reg_parser.add_argument('password', help='This field cannot be blank', required=True)
reg_parser.add_argument('char_name', help='This field cannot be blank', required=True)
reg_parser.add_argument('email', help='This field cannot be blank', required=True)

log_parser = reqparse.RequestParser()
log_parser.add_argument('username', help='This field cannot be blank', required=True)
log_parser.add_argument('password', help='This field cannot be blank', required=True)

fight_parser = reqparse.RequestParser()
fight_parser.add_argument('attacker_id', help='This field cannot be blank', required=True)
fight_parser.add_argument('defender_id', help='This field cannot be blank', required=True)

trader_parser = reqparse.RequestParser()
trader_parser.add_argument('bp_id', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = reg_parser.parse_args()
        username = data['username']
        char_name = data['char_name']

        if User.find_user_by_name(username):
            return {'success': False, 'message': 'User {} already exists.'.format(username)}

        if Character.find_by_name(char_name):
            print(Character.find_by_name(char_name))
            return {'success': False, 'message': 'Character {} already exists.'.format(char_name)}

        if '@' not in data['email'] or '.' not in data['email']:
            return {'success': False, 'message': 'Invalid email.'}

        new_user = User(
            name=username,
            password=data['password'],
            email=data['email']
        )
        try:
            user_id = new_user.save()
            create_default_character(char_name, user_id)

            access_token = create_access_token(identity=user_id)
            refresh_token = create_refresh_token(identity=user_id)
            return {
                'success': True,
                'message': 'User {} successfully created.'.format(username),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'redirect_url': 'localhost:5000'
            }
        except Exception as e:
            print(str(e))
            return {'success': False, 'message': 'Something went wrong, please try again.'}


class UserLogin(Resource):
    def post(self):
        data = log_parser.parse_args()
        username = data['username']
        current_user = User.find_user_by_name(username)

        if not current_user:
            return {'success': False, 'message': "User {} doesn't exist.".format(username)}
        if current_user.check_password(data['password']):
            access_token = create_access_token(identity=current_user.id)
            refresh_token = create_refresh_token(identity=current_user.id)
            print(calculate_stats('Nothy'))
            return {
                'success': True,
                'message': 'Logged in successfully.',
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        else:
            return {'success': False, 'message': 'Wrong password.'}


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {
                'success': True,
                'message': 'Access token revoked.',
                'goto': 'localhost:5000',
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'success': False, 'message': 'Refresh token has been revoked'}
        except:
            return {'success': False, 'message': 'Something went wrong'}

# VIEWS


class CharacterView(Resource):
    @jwt_required
    def get(self):
        char = Character.find_by_id(int(get_jwt_identity()), todict=True)
        items = Character['itemsingame']
        items = [item.to_dict() for item in items]
        char = calculate_stats(int(get_jwt_identity()))
        if char:
            response = {'success': True}
            response.update(char)
            response.update({'items': items})
            return response
        else:
            return {'success': False, 'message': 'This character does not exist.'}


class ArenaView(Resource):
    @jwt_required
    def get(self):
        characters_num = db.session.query(Character).count()
        enemy = random.randint(1, characters_num)
        while enemy == get_jwt_identity():
            enemy = random.randint(1, characters_num)
        enemy = Character.find_by_id(enemy, todict=True)
        enemy_items = enemy.pop('items_in_game')
        enemy_items = [item.to_dict() for item in enemy_items]
        enemy.update({'items_in_game': enemy_items})
        return {'success': True, 'enemy': enemy}


class ExpeditionView(Resource):
    @jwt_required
    def get(self):
        enemies_num = db.session.query(Enemy).count()
        enemy = random.randint(1, enemies_num)
        enemy = Enemy.query.filter_by(id=enemy).first().to_dict()
        response = {'success': True, }


class HealerView(Resource):
    @jwt_required
    def get(self):
        char, text = get_stats_npc(get_jwt_identity(), healer=True)
        price = (char['max_health'] - char['health']) * 10
        response = {
            'success': True,
            'health': char['health'],
            'max_health': char['max_health'],
            'text': text,
            'price': price,
        }
        return response


class TraderView(Resource):
    @jwt_required
    def get(self):
        char, text = get_stats_npc(get_jwt_identity(), trader=True)
        blueprints_num = db.session.query(Blueprint).count()
        trader_items = []
        while len(trader_items) < 6:
            trader_items.append(Blueprint.find_by_id(random.randint(1, blueprints_num)).to_dict())
        response = {
            'success': True,
            'money': char['money'],
            'items': trader_items,
        }


# FIGHTS

class CharacterFight(Resource):
    @jwt_required
    def post(self):
        characters = fight_parser.parse_args()
        return run_fight(int(get_jwt_identity()), d_char=int(characters['defender_id']))


class MonsterFight(Resource):
    @jwt_required
    def post(self):
        characters = fight_parser.parse_args()
        return run_fight(int(get_jwt_identity()), enemy=int(characters['defender_id']))


# NPC


class HealerHeal(Resource):
    @jwt_required
    def get(self):
        char = Character.find_by_id(id=int(get_jwt_identity())).to_dict()
        price = (char['max_health'] + char['health']) * 10
        if char['money'] < price:
            return {'success': False, 'message': "You don't have enough gold."}
        else:
            char.edit(gold=(price * -1))
            char.edit(health=char['max_health'])
            db.session.commit()
            return {
                'success': True,
                'paid': price,
                'gold_left': char['money'],
                'health': char['health'],
                'max_health': char['max_health'],
            }


class TraderBuy(Resource):
    @jwt_required
    def get(self):
        char = Character.find_by_id(id=int(get_jwt_identity())).to_dict()
        choice = trader_parser.parse_args()['bp_id']
        item = Blueprint.find_by_id(int(choice)).to_dict()
        if char['money'] < item['price']:
            return {'success': False, 'message': "You don't have enough gold."}
        else:
            price = item['price']
            slot = item['slot']
            to_replace = ItemsInGame.query.filter_by(character_id=int(get_jwt_identity()), slot=slot).first()
            to_replace_stats = to_replace.to_dict()
            price -= int(Blueprint.find_by_id(to_replace_stats['bp_id']).to_dict()['price'] * 0.5)
            new_item = ItemsInGame(
                slot=slot,
                blueprint_id=item['id'],
                character_id=get_jwt_identity(),
            )
            char.edit(gold=(-1 * price))
            db.session.delete(to_replace)
            db.session.add(new_item)
            db.session.commit()








