from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(60), unique=True, nullable=False)
    name = db.Column('user_name', db.String(35), unique=True, nullable=False)
    password_hash = db.Column('password_hash', db.String(128))
    create_date = db.Column('create_date', db.DateTime, default=datetime.now())

    character = db.relationship('Character', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<{}, name: {}.'.format(self.id, self.name)


class Character(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    char_name = db.Column('char_name', db.String(45), unique=True, nullable=False)

    health = db.Column('health', db.Integer, nullable=False)
    strength = db.Column('strength', db.Integer, nullable=False)
    reflex = db.Column('reflex', db.Integer, nullable=False)
    charisma = db.Column('charisma', db.Integer, nullable=False)
    intelligence = db.Column('intelligence', db.Integer, nullable=False)
    will = db.Column('will', db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    itemsingame = db.relationship('ItemsInGame', backref='character', lazy=True)

    image_path = db.Column('img_path', db.String(128), nullable=False)

    def __repr__(self):
        return 'id: {}, char_name: {}, health: {}, strength: {}, reflex: {}, ' \
               'charisma: {}, intelligence: {}, will: {}, user_id: {}, itemsingame: {}, image_path:{}'.format(
            self.id, self.char_name, self.health, self.strength, self.reflex, self.charisma,
            self.intelligence, self.will, self.user_id, self.itemsingame, self.image_path
        )


class Blueprint(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)

    health = db.Column('health', db.Integer, nullable=False)
    strength = db.Column('strength', db.Integer, nullable=False)
    reflex = db.Column('reflex', db.Integer, nullable=False)
    charisma = db.Column('charisma', db.Integer, nullable=False)
    intelligence = db.Column('intelligence', db.Integer, nullable=False)
    will = db.Column('will', db.Integer, nullable=False)
    armor = db.Column('armor', db.Integer, nullable=False)
    min_dmg = db.Column('min_dmg', db.Integer, nullable=False)
    max_dmg = db.Column('max_dmg', db.Integer, nullable=False)

    image_path = db.Column('img_path', db.String(128), nullable=False)
    items_in_game = db.relationship('ItemsInGame', backref='blueprint')


class ItemsInGame(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    slot = db.Column('slot', db.Integer, nullable=False)
    name = db.Column('iig_name', db.String(35), nullable=False)
    equipped = db.Column('equipped', db.Boolean)
    blueprint_id = db.Column('bp_id', db.Integer, db.ForeignKey('blueprint.id'))
    character_id = db.Column('char_id', db.Integer, db.ForeignKey('character.id'))


class Enemy(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('enemy_name', db.String(35), unique=True, nullable=False)
    rarity = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Integer, nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    reflex = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    will = db.Column(db.Integer, nullable=False)

    armor = db.Column(db.Integer, nullable=False)
    min_dmg = db.Column(db.Integer, nullable=False)
    max_dmg = db.Column(db.Integer, nullable=False)

    image_path = db.Column('img_path', db.String(128), nullable=False)


class NonPersonCharacter(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('npc_name', db.String(35), unique=True, nullable=False)
    healer = db.Column(db.Boolean)
    trader = db.Column(db.Boolean)
    text1 = db.Column(db.Text)
    text2 = db.Column(db.Text)
    text3 = db.Column(db.Text)
    image_path = db.Column('img_path', db.String(128), nullable=False)
