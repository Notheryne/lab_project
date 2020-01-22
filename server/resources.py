from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, \
    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, jwt_optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text as text_query

from server.db_models.User import User
from server.db_models.RevokedTokenModel import RevokedTokenModel
from server.db_models.Character import Character
from server.db_models.Enemy import Enemy
from server.db_models.NonPersonCharacter import NonPersonCharacter

from server.db_models.defaults import create_default_character
from server.func_resources import *


def get_current_user(id_only=False):
    user = User.find_user_by_id(int(get_jwt_identity()))
    if id_only:
        return user.id
    return user


# Initializing parsers of arguments.

register_endpoint_parser = reqparse.RequestParser()
register_endpoint_parser.add_argument('username', help='This field cannot be blank', required=True)
register_endpoint_parser.add_argument('email', help='This field cannot be blank', required=True)
register_endpoint_parser.add_argument('char_name', help='This field cannot be blank', required=True)
register_endpoint_parser.add_argument('password', help='This field cannot be blank', required=True)

login_endpoint_parser = reqparse.RequestParser()
login_endpoint_parser.add_argument('username', help='This field cannot be blank', required=True)
login_endpoint_parser.add_argument('password', help='This field cannot be blank', required=True)

token_validation_parser = reqparse.RequestParser()
token_validation_parser.add_argument('access_token', help='This field cannot be blank', required=True)

fight_endpoint_parser = reqparse.RequestParser()
fight_endpoint_parser.add_argument('defender_id', help='This field cannot be blank', required=True)

trader_endpoint_parser = reqparse.RequestParser()
trader_endpoint_parser.add_argument('bp_id', help='This field cannot be blank', required=True)

change_user_data_parser = reqparse.RequestParser()
change_user_data_parser.add_argument('stat_name', help='This field cannot be blank', required=True)
change_user_data_parser.add_argument('value', help='This field cannot be blank', required=True)

ranking_parser = reqparse.RequestParser()
ranking_parser.add_argument('sort_by')
ranking_parser.add_argument('order')
ranking_parser.add_argument('page')
ranking_parser.add_argument('minimum_value')

# PARSER TO ADD NEW OBJECTS VIA API
add_stats_endpoint_parser = reqparse.RequestParser()
add_stats_endpoint_parser.add_argument('stat', help='This field cannot be blank', required=True)

add_blueprint_endpoint_parser = reqparse.RequestParser()
add_blueprint_endpoint_parser.add_argument('slot', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('name', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('price', help='This field cannot be blank', required=True)
add_blueprint_endpoint_parser.add_argument('max_health', help='This field cannot be blank', required=True)
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
        email = data['email']
        if username == '':
            return {'success': False, 'message': "Field 'Username' can't be empty."}, 400

        if email == '':
            return {'success': False, 'message': "Field 'Email' can't be empty."}, 400

        if '@' not in email or '.' not in email or ' ' in email:
            return {'success': False, 'message': 'Invalid email.'}, 400

        if char_name == '':
            return {'success': False, 'message': "Field 'Character Name' can't be empty."}, 400

        if data['password'] == '':
            return {'success': False, 'message': "Field 'Password' can't be empty."}, 400

        if User.find_user_by_name(username):
            return {'success': False, 'message': 'User {} already exists.'.format(username)}, 400

        if User.find_user_by_email(email):
            return {'success': False, 'message': 'User with email address {} already exists.'.format(email)}, 400

        if Character.find_by_name(char_name):
            return {'success': False, 'message': 'Character {} already exists.'.format(char_name)}, 400

        new_user = User(
            name=username,
            password=data['password'],
            email=data['email']
        )
        created = dict.fromkeys(['user', 'char'])
        try:
            user_id = new_user.save()
            created['user'] = user_id
            new_char, default_sword, default_shield = create_default_character(char_name, user_id)
            new_char.save()
            created['char'] = new_char.id

            ItemsInGame(**default_sword, character_id=new_char.id).save()
            ItemsInGame(**default_shield, character_id=new_char.id).save()

            access_token = create_access_token(identity=user_id)
            refresh_token = create_refresh_token(identity=user_id)
            return {
                'success': True,
                'message': 'User {} successfully created.'.format(username),
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        except Exception as e:
            if created['char']:
                char = Character.find_by_id(created['char'])
                items = char.itemsingame
                for item in items:
                    db.session.delete(item)
                db.session.delete(char)
            if created['user']:
                db.session.delete(User.find_user_by_id(created['user']))
            db.session.commit()
            return {'success': False, 'message': 'Something went wrong, please try again.',
                    'error_message': str(e)}, 400


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
            if len(username) > 0:
                return {'success': False, 'message': "User {} doesn't exist.".format(username)}, 400
            else:
                return {'success': False, 'message': "Field 'Username' cannot be empty."}, 400
        if current_user.check_password(data['password']):
            access_token = create_access_token(identity=current_user.id)
            refresh_token = create_refresh_token(identity=current_user.id)
            return {
                'success': True,
                'message': 'Logged in successfully.',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'redirect': '/character'
            }
        else:
            return {'success': False, 'message': 'Wrong password.'}, 400


class Refresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        user_id = get_current_user(id_only=True)
        if user_id:
            return {
                'access_token': create_access_token(identity=user_id),
                'refresh_token': create_refresh_token(identity=user_id)
            }
        else:
            return {'success': False, 'message': 'Refresh token not recognized.'}, 400


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
            revoked_token.save()
            return {
                'success': True,
                'message': 'Access token revoked.',
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
            revoked_token.save()
            return {'success': True, 'message': 'Refresh token has been revoked'}
        except:
            return {'success': False, 'message': 'Something went wrong'}, 400


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
        user = get_current_user()
        char = user.character[0]
        free_stats = char.free_stats
        char = char.to_dict()
        items = char['items_in_game']
        items = [item.to_dict()['bp_id'] for item in items]
        items = [Blueprint.find_by_id(item).to_dict_stats() for item in items]
        items = {item['slot']: item for item in items}
        char = calculate_stats(char['id'])
        if char:
            response = {'success': True}
            response.update(char)
            response.update({'free_stats': free_stats})
            response.update({'items': items})
            return response
        else:
            return {'success': False, 'message': 'This character does not exist.'}, 400


class ArenaView(Resource):
    """

    action: get random character enemy
    location: /api/arena
    methods: get
    return: json with status and all enemy attributes
    """

    @jwt_required
    def get(self):
        user = get_current_user()
        char = user.character[0]
        characters_num = db.session.query(Character).count()
        enemy = random.randint(1, characters_num)
        while enemy == char.id:
            enemy = random.randint(1, characters_num)
        enemy_id = int(enemy)
        enemy = Character.find_by_id(enemy, todict=True)
        items = enemy['items_in_game']
        items = [item.to_dict()['bp_id'] for item in items]
        items = [Blueprint.find_by_id(item).to_dict_stats() for item in items]
        items = {item['slot']: item for item in items}
        enemy = calculate_stats(enemy['id'])
        enemy.update({'id': enemy_id})
        enemy.update({'items': items})
        return {
            'success': True,
            'enemy': enemy
        }


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
        user = get_current_user()
        text, img_path, npc_name = get_stats_npc(healer=True)
        char = user.character[0]
        price = (char.max_health - char.health) * 10
        response = {
            'success': True,
            'name': npc_name,
            'img_path': img_path,
            'health': char.health,
            'max_health': char.max_health,
            'text': text,
            'price': price,
            'char_gold': char.gold,
        }
        return response


class TraderView(Resource):
    """

    action: view trader NPC, items and prices
    location: /api/npc/trader
    methods: get
    return: json with status, text, items attributes and prices
    """

    @jwt_required
    def get(self):
        user = get_current_user()
        char_id = user.character[0].id
        char, text, img_path, npc_name = get_stats_npc(char_id, trader=True)
        blueprints_num = db.session.query(Blueprint).count()
        trader_items = []
        taken_ids = []
        while len(trader_items) < 6:
            random_id = random.randint(91, blueprints_num)
            if random_id not in taken_ids:
                item = Blueprint.find_by_id(random_id).to_dict()
                del item['iig']
                trader_items.append(item)
                taken_ids.append(random_id)
        return {
            'success': True,
            'name': npc_name,
            'img_path': img_path,
            'gold': char['gold'],
            'text': text,
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
        user = get_current_user()
        user = user.to_dict()
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
        defender_id = fight_endpoint_parser.parse_args()['defender_id']
        user = get_current_user()
        char = user.character[0]
        fight = run_fight(a_char=char.id, d_char=int(defender_id))
        if fight['success']:
            return fight
        return fight, 400


class MonsterFight(Resource):
    """

    action: run a fight between identified character and passed enemy
    location: /api/expedition/fight
    methods: post
    return: json with fight course and result
    """

    @jwt_required
    def post(self):
        defender_id = fight_endpoint_parser.parse_args()['defender_id']
        user = get_current_user()
        char = user.character[0]
        fight = run_fight(a_char=char.id, enemy=int(defender_id))
        if fight['success']:
            return fight
        return fight, 400


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
        user = get_current_user()
        char = user.character[0]
        price = (char.max_health - char.health) * 10
        if char.gold < price:
            return {'success': False, 'message': "You don't have enough gold."}, 400
        else:
            char.edit(gold=(price * -1))
            starting_health = char.health
            char.edit(health=char.max_health)
            db.session.commit()
            return {
                'success': True,
                'paid': price,
                'gold_left': char.gold,
                'healed_for': char.max_health - starting_health,
                'health': char.health,
                'max_health': char.max_health,
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
        user = get_current_user()
        char = user.character[0]
        choice = trader_endpoint_parser.parse_args()['bp_id']
        item = Blueprint.find_by_id(int(choice))
        if char.gold < item.price:
            return {'success': False, 'message': "You don't have enough gold."}, 400
        else:
            price = item.price
            slot = item.slot
            to_replace = ItemsInGame.query.filter_by(character_id=char.id, slot=slot).first()
            if to_replace:
                to_replace_stats = to_replace.to_dict()
                db.session.delete(to_replace)
                refund = Blueprint.find_by_id(to_replace_stats['bp_id']).price
                refund = int(int(refund) * 0.5)
            else:
                refund = 0
            price -= refund
            new_item = ItemsInGame(
                slot=slot,
                blueprint_id=item.id,
                character_id=char.id,
            )
            char.edit(gold=(-1 * price))
            db.session.add(new_item)
            db.session.commit()
            return {
                'success': True,
                'item': choice,
                'character': char.id,
                'paid_gold': item.price,
                'returned_gold': abs(price - item.price),
                'gold_left': char.gold
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
        user = get_current_user()
        char = user.character[0]
        stat = add_stats_endpoint_parser.parse_args()['stat']
        response = char.add_stat(stat=stat)
        if response['success']:
            char.save()
            return response
        return response, 400


# RANKING
class Ranking(Resource):
    sortable = {
        'level': Character.level,
        'experience': Character.experience,
        'max_health': Character.max_health,
        'strength': Character.strength,
        'reflex': Character.reflex,
        'charisma': Character.charisma,
        'intelligence': Character.intelligence,
        'will': Character.will,
        'create_date': User.create_date,
        'total': None
    }
    possible_orders = ['asc', 'desc']

    def get(self):
        results_per_page = 30
        characters_num = db.session.query(Character).count()
        max_pages = math.ceil(characters_num / results_per_page)

        data = ranking_parser.parse_args()

        sort_by = data['sort_by'].lower() if data['sort_by'] and data['sort_by'] != '' else 'experience'
        if sort_by not in self.sortable:
            return {'success': False, 'message': 'Unknown "sort_by" parameter.'}, 400

        try:
            page = int(data['page']) if data['page'] and int(data['page']) >= 0 else 1
        except ValueError:
            return {'success': False, 'message': 'Wrong "page" parameter.'}, 400
        if page > max_pages:
            return {'success': False, 'message': 'Wrong "page" parameter.'}
        start = (page - 1) * results_per_page

        order = data['order'].lower() if data['order'] else 'desc'
        if order not in self.possible_orders:
            return {'success': False, 'message': 'Wrong "order" parameter'}, 400

        try:
            minimum_value = int(data['minimum_value']) \
                if data['minimum_value'] and int(data['minimum_value']) >= 0 else 0
        except ValueError:
            return {'success': False, 'message': 'Wrong "minimum_value" parameter.'}, 400

        if (start + results_per_page) < characters_num:
            more_records_in_database = True
        else:
            more_records_in_database = False

        characters = {}
        if sort_by != "total":
            # """
            # SELECT c.character_name, c.`level`, c.experience, c.max_health, c.strength,
            # c.reflex, c.charisma, c.intelligence, c.will, u.create_date, u.id
            # FROM `character` as c, `user` as u
            # WHERE c.user_id = u.id
            # ORDER BY @sort_by DESC;
            # """
            query = db.session.query().with_entities(Character.name, Character.level, Character.experience,
                                                     Character.max_health, Character.strength,
                                                     Character.reflex, Character.charisma, Character.intelligence,
                                                     Character.will, User.create_date)
            if order == 'asc':
                query = query.order_by(self.sortable[sort_by].asc())
            else:
                query = query.order_by(self.sortable[sort_by].desc())
            query = query.filter(Character.user_id == User.id)
            query = query.offset(start).limit(results_per_page)
            results = query.all()
            results = [row._asdict() for row in results]
        else:
            get_total_query = text_query("""
                SELECT the_richest_players.character_name AS name, the_richest_players.level,
                the_richest_players.experience, the_richest_players.max_health,
                the_richest_players.strength, the_richest_players.reflex, the_richest_players.charisma, 
                the_richest_players.intelligence, the_richest_players.will,
                u.create_date, the_richest_players.items_value + the_richest_players.money AS total
                 FROM (
                    SELECT SUM(price) AS items_value, c.character_name, c.`level`, c.experience, c.money,
                    c.max_health, c.strength, c.reflex, c.charisma, c.intelligence, c.will, c.user_id AS id
                    FROM items_in_game as iig
                    INNER JOIN blueprint as bp
                    ON iig.blueprint_id = bp.id
                    INNER JOIN `character` as c
                    ON iig.character_id = c.id
                    GROUP BY iig.character_id
                    HAVING items_value >= :minimum_value
                ) AS the_richest_players
                INNER JOIN `user` as u
                ON the_richest_players.id = u.id
                ORDER BY items_value {}
                LIMIT :results_per_page
                OFFSET :start
                """.format(order))
            get_total_query = get_total_query.bindparams(
                minimum_value=minimum_value,
                start=start,
                results_per_page=results_per_page
            )
            results = db.engine.execute(get_total_query).fetchall()
            results = [dict(row) for row in results]

        i = start + 1
        for char_dict in results:
            char_dict['create_date'] = str(char_dict['create_date'])[:19]
            if 'total' in char_dict:
                char_dict['total'] = float(char_dict['total'])
            else:
                char_dict['total'] = '-'
            characters[i] = char_dict
            i += 1

        return {
            'success': True,
            'more_records': more_records_in_database,
            'next_page': page + 1 if more_records_in_database else None,
            'last_page': max_pages,
            'characters': characters
        }


# DATABASE MANAGEMENT
class AccountManage(Resource):
    """

    """

    @jwt_required
    def post(self):
        data = change_user_data_parser.parse_args()
        user = get_current_user()
        if data['stat_name'] == 'character_name':
            char = user.character[0]
            return char.set_character_name(data['value'])
        elif data['stat_name'] == 'email':
            return user.set_email(data['value'])
        else:
            print("HERE")
            return {'success': False, 'message': 'Parameter "stat_name" not recognized.'}, 400

    @jwt_required
    def delete(self):
        user = get_current_user()
        char = user.character[0]
        items_in_game = char.itemsingame
        jti = get_raw_jwt()['jti']

        try:
            # START TRANSACTION
            # delete characters' items
            for item in items_in_game:
                db.session.delete(item)
            # delete character
            db.session.delete(char)
            # revoke token from user
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.save()
            # delete token
            db.session.delete(user)

            # commit changes
            db.session.commit()
            return {'success': True, 'message': 'Account successfully deleted.'}
        except Exception as e:
            # IN CASE SOMETHING GOES WRONG, ROLL DATABASE BACK
            db.session.rollback()
            return {'success': False, 'message': 'Account has not been deleted.', 'error_message': str(e)}, 400


# UserRegistration


class AddItem(Resource):
    """

    action: create new item and save it in database
    location: api/add/item
    methods: post
    return: status and item info
    """

    # @jwt_required
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
