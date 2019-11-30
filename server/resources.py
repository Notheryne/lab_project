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


# Initializing parsers of arguments.

register_endpoint_parser = reqparse.RequestParser()
register_endpoint_parser.add_argument('username', help='This field cannot be blank', required=True)
register_endpoint_parser.add_argument('email', help='This field cannot be blank', required=True)
register_endpoint_parser.add_argument('char_name', help='This field cannot be blank', required=True)
register_endpoint_parser.add_argument('password', help='This field cannot be blank', required=True)

login_endpoint_parser = reqparse.RequestParser()
login_endpoint_parser.add_argument('username', help='This field cannot be blank', required=True)
login_endpoint_parser.add_argument('password', help='This field cannot be blank', required=True)

fight_endpoint_parser = reqparse.RequestParser()
fight_endpoint_parser.add_argument('attacker_id', help='This field cannot be blank', required=True)
fight_endpoint_parser.add_argument('defender_id', help='This field cannot be blank', required=True)

trader_endpoint_parser = reqparse.RequestParser()
trader_endpoint_parser.add_argument('bp_id', help='This field cannot be blank', required=True)

# PARSER TO ADD NEW OBJECTS VIA API
add_stats_endpoint_parser = reqparse.RequestParser()
add_stats_endpoint_parser.add_argument('stat', help='This field cannot be blank', required=True)


add_blueprint_endpoint_parser = reqparse.RequestParser()
add_blueprint_endpoint_parser.add_argument('slot', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('name', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('price', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('health', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('strength', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('reflex', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('charisma', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('intelligence', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('will', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('armor', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('min_dmg', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('max_dmg', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('image_path', help='This field cannot be blank', required=True)


add_item_endpoint_parser = reqparse.RequestParser()
add_item_endpoint_parser.add_argument('blueprint_id', help='This field cannot be blank', required=True)
add_item_endpoint_parser.add_argument('character_id', help='This field cannot be blank', required=True)


add_enemy_endpoint_parser = reqparse.RequestParser()
add_enemy_endpoint_parser.add_argument('name', help='This field cannot be blank', required=True)
add_enemy_endpoint_parser.add_argument('experience', help='This field cannot be blank', required=True)
add_enemy_endpoint_parser.add_argument('gold', help='This field cannot be blank', required=True)
add_enemy_endpoint_parser.add_argument('health', help='This field cannot be blank', required=True)
add_enemy_endpoint_parser.add_argument('strength', help='This field cannot be blank', required=True)
add_enemy_endpoint_parser.add_argument('reflex', help='This field cannot be blank', required=True)
add_enemy_endpoint_parser.add_argument('charisma', help='This field cannot be blank', required=True)
add_enemy_endpoint_parser.add_argument('intelligence', help='This field cannot be blank', required=True)
add_enemy_endpoint_parser.add_argument('will', help='This field cannot be blank', required=True)
add_enemy_endpoint_parser.add_argument('armor', help='This field cannot be blank', required=True)
add_enemy_endpoint_parser.add_argument('min_dmg', help='This field cannot be blank', required=True)
add_enemy_endpoint_parser.add_argument('max_dmg', help='This field cannot be blank', required=True)
add_enemy_endpoint_parser.add_argument('image_path', help='This field cannot be blank', required=True)


# USER MANAGEMENT


class UserRegistration(Resource):
    """

    action: register new user, add new character and starter items to it
    location: /api/register
    methods: post
    return: json with status, message, acces token, refresh token and url to go to
    """
    def post(self):
        data = register_endpoint_parser.parse_args()
        username = data['username']
        char_name = data['char_name']

        if username == '':
            return {'success': False, 'message': "Field 'Username' can't be empty."}

        if data['email'] == '':
            return {'success': False, 'message': "Field 'Email' can't be empty."}

        if char_name == '':
            return {'success': False, 'message': "Field 'Character Name' can't be empty."}

        if data['password'] == '':
            return {'success': False, 'message': "Field 'Password' can't be empty."}

        if User.find_user_by_name(username):
            return {'success': False, 'message': 'User {} already exists.'.format(username)}

        if Character.find_by_name(char_name):
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
                'redirect_url': 'http://localhost:8080/#/'
            }
        except Exception as e:
            print(str(e))
            return {'success': False, 'message': 'Something went wrong, please try again.'}


class UserLogin(Resource):
    """

    action: login user
    location: /api/login
    methods: post
    return: json with status, message, acces token, refresh token and url to go to
    """
    def post(self):
        data = login_endpoint_parser.parse_args()
        username = data['username']
        current_user = User.find_user_by_name(username)

        if not current_user:
            return {'success': False, 'message': "User {} doesn't exist.".format(username)}
        if current_user.check_password(data['password']):
            access_token = create_access_token(identity=current_user.id)
            refresh_token = create_refresh_token(identity=current_user.id)
            return {
                'success': True,
                'message': 'Logged in successfully.',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'redirect_url': 'http://localhost:8080/#/'
            }
        else:
            return {'success': False, 'message': 'Wrong password.'}


class UserLogout(Resource):
    """

    action: logout user (blacklist his access token)
    location: /api/logout
    methods: post
    json with status, message and url to go to
    """
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
    """

    action: logout user (blacklist his refresh token)
    location: /api/logout/refresh
    methods: post
    return: json with status and message
    """
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'success': True, 'message': 'Refresh token has been revoked'}
        except:
            return {'success': False, 'message': 'Something went wrong'}

# VIEWS


class CharacterView(Resource):
    """

    action: view character stats
    location: /api/character
    methods: get
    return: json with status and all character attributes
    """
    @jwt_required
    def get(self):
        char = Character.find_by_id(int(get_jwt_identity()), todict=True)
        print(char)
        items = char['items_in_game']
        items = [item.to_dict() for item in items]
        char = calculate_stats(int(get_jwt_identity()))
        print(get_jwt_identity())
        if char:
            response = {'success': True}
            response.update(char)
            response.update({'items': items})
            return response
        else:
            return {'success': False, 'message': 'This character does not exist.'}


class ArenaView(Resource):
    """

    action: get random character enemy
    location: /api/arena
    methods: get
    return: json with status and all enemy attributes
    """
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
    """

    action: get random enemy
    location: /api/expedition
    methods: get
    return: json with status and all enemy attributes
    """
    @jwt_required
    def get(self):
        enemies_num = db.session.query(Enemy).count()
        enemy = random.randint(1, enemies_num)
        enemy = Enemy.query.filter_by(id=enemy).first().to_dict()
        return {'success': True, 'enemy': enemy}


class HealerView(Resource):
    """

    action: view healer NPC, healing price
    location: /api/npc/healer
    methods: get
    return: json with status, text and price
    """
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
    """

    action: view trader NPC, items and prices
    location: /api/npc/trader
    methods: get
    return: json with status, text, items attributse and prices
    """
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


class AccountManageView(Resource):
    """

    action: view possibility of managing user
    location: /api/manage
    methods: get
    return: json with status and all user info except password
    """
    @jwt_required
    def get(self):
        user = User.query.filter_by(id=int(get_jwt_identity())).to_dict()
        del user['password_hash']
        response = {'success': True}
        response.update(user)
        return response


# FIGHTS

class CharacterFight(Resource):
    """

    action: run a fight between identified character and passed enemy character
    location: /api/arena/fight
    methods: post
    return: json with fight course and result
    """
    @jwt_required
    def post(self):
        characters = fight_endpoint_parser.parse_args()
        return run_fight(int(get_jwt_identity()), d_char=int(characters['defender_id']))


class MonsterFight(Resource):
    """

    action: run a fight between identified character and passed enemy
    location: /api/expedition/fight
    methods: post
    return: json with fight course and result
    """
    @jwt_required
    def post(self):
        characters = fight_endpoint_parser.parse_args()
        return run_fight(int(get_jwt_identity()), enemy=int(characters['defender_id']))


# NPC


class HealerHeal(Resource):
    """

    action: make user health his max health
    location: /api/npc/heal
    methods: post
    return: json with status and transaction information, health status
    """
    @jwt_required
    def post(self):
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
    """

    action: add new item to character and remove the old one in slot
    location: /api/npc/trade
    methods: post
    return: json with status, transaction info and character gold status
    """
    @jwt_required
    def post(self):
        char = Character.find_by_id(id=int(get_jwt_identity())).to_dict()
        choice = trader_endpoint_parser.parse_args()['bp_id']
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
            return {
                'success': True,
                'item': choice,
                'character': int(get_jwt_identity()),
                'paid_gold': item['price'],
                'returned_gold': abs(price-item['price']),
                'gold_left': char['gold']
            }

# STATS


class AddStat(Resource):
    """

    action: increase chosen stat
    location: /add/stats
    methods:
    return:
    """
    @jwt_required
    def post(self):
        char = Character.find_by_id(int(get_jwt_identity()))
        stat = str(add_stats_endpoint_parser.parse_args()['stat'])
        response = char.add_stat(stat=stat)
        if response['success']:
            db.session.commit()
        return response


# DATABASE MANAGEMENT


# UserRegistration


class AddItem(Resource):
    """

    action: create new item and save it in database
    location: api/add/item
    methods: post
    return: status and item info
    """
    @jwt_required
    def post(self):
        data = add_item_endpoint_parser.parse_args()
        blueprint = Blueprint.find_by_id(int(data['blueprint_id'])).to_dict()
        new_item = ItemsInGame(
            slot=blueprint['slot'],
            blueprint_id=int(data['blueprint_id']),
            character_id=int(data['character_id']),
        )

        new_item.save()
        return {
            'success': True,
            'item': new_item.to_dict()
        }


class AddBlueprint(Resource):
    """

    action: create new blueprint and save it in database
    location: api/add/blueprint
    methods: post
    return: status and blueprint info
    """
    @jwt_required
    def post(self):
        data = add_blueprint_endpoint_parser.parse_args()
        new_blueprint = Blueprint(**data)
        new_blueprint.save()
        return {
            'success': True,
            'blueprint': new_blueprint.to_dict()
        }


class AddEnemy(Resource):
    """

    action: create new enemy and save it in database
    location: api/add/enemy
    methods: post
    return: status and enemy info
    """
    @jwt_required
    def post(self):
        data = add_enemy_endpoint_parser.parse_args()
        new_enemy = Enemy(**data)
        new_enemy.save()
        return {
            'success': True,
            'enemy': new_enemy.to_dict(),
        }
