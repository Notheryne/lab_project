from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, \
    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt

from server.db_models.User import User
from server.db_models.RevokedTokenModel import RevokedTokenModel
from server.db_models.Character import Character
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


class UserRegistration(Resource):
    def post(self):
        data = reg_parser.parse_args()
        username = data['username']
        char_name = data['char_name']

        if User.find_user_by_name(username):
            return {'message': 'User {} already exists.'.format(username)}

        if Character.find_character_by_name(char_name):
            print(Character.find_character_by_name(char_name))
            return {'message': 'Character {} already exists.'.format(char_name)}

        if '@' not in data['email'] or '.' not in data['email']:
            return {'message': 'Invalid email.'}

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
                'message': 'User {} successfully created.'.format(username),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'redirect_url': 'localhost:5000'
            }
        except Exception as e:
            print(str(e))
            return {'message': 'Something went wrong, please try again.'}


class UserLogin(Resource):
    def post(self):
        data = log_parser.parse_args()
        username = data['username']
        current_user = User.find_user_by_name(username)

        if not current_user:
            return {'message': "User {} doesn't exist.".format(username)}
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
            return {'message': 'Wrong password.'}


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {
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
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class CharacterFight(Resource):
    @jwt_required
    def post(self):
        print(get_jwt_identity())
        characters = fight_parser.parse_args()
        return run_fight(int(characters['attacker_id']), int(characters['defender_id']))


