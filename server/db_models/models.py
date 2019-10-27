from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(60), unique=True, nullable=False)
    name = db.Column('user_name', db.String(35), unique=True, nullable=False)
    password_hash = db.Column('password_hash', db.String(128))
    create_date = db.Column('create_date', db.DateTime, default=datetime.now())

    character = db.relationship('character', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<{}, name: {}.'.format(self.id, self.name)


class Character(db.Model):
    id = db.Column('char_id', db.Integer, primary_key=True)
    char_name = db.Column('char_name', db.String(45), unique=True, nullable=False)

    health = db.Column('health', db.Integer, nullable=False)
    strength = db.Column('strength', db.Integer, nullable=False)
    reflex = db.Column('reflex', db.Integer, nullable=False)
    charisma = db.Column('charisma', db.Integer, nullable=False)
    intelligence = db.Column('intelligence', db.Integer, nullable=False)
    will = db.Column('will', db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), unique=True, nullable=False)
    user = db.relationship('user', backref='character', lazy=True)

    image_path = db.Column('img_path', db.String(128))


class Blueprints(db.Model):
    bp_id = db.Column('bp_id', db.Integer, primary_key=True)
    bp_type = db.Column(db.Integer, nullable=False)

    health = db.Column('health', db.Integer, nullable=False)
    strength = db.Column('strength', db.Integer, nullable=False)
    reflex = db.Column('reflex', db.Integer, nullable=False)
    charisma = db.Column('charisma', db.Integer, nullable=False)
    intelligence = db.Column('intelligence', db.Integer, nullable=False)
    will = db.Column('will', db.Integer, nullable=False)
    armor = db.Column('armor', db.Integer, nullable=False)
    min_dmg = db.Column('min_dmg', db.Integer, nullable=False)
    max_dmg = db.Column('max_dmg', db.Integer, nullable=False)

    image_path = db.Column('img_path', db.String(128))


class ItemsInGame(db.Model):
    iig_id = db.Column('iig_id', db.Integer, primary_key=True)
    slot = db.Column('slot', db.Integer, nullable=False)
    name = db.Column('iig_name', db.String(35), nullable=False)
    equipped = db.Column('equipped', db.Boolean)
    blueprint_id = db.Column('bp_placeholder', db.Integer())
    character_id = db.Column('char_placeholder', db.Integer())


class Enemy(db.Model):
    enemy_id = db.Column('enemy_id', db.Integer, primary_key=True)
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

    image_path = db.Column(db.String(128))


class NonPersonCharacter(db.Model):
    npc_id = db.Column('npc_id', db.Integer, primary_key=True)
    name = db.Column('npc_name', db.String(35), unique=True, nullable=False)
    healer = db.Column(db.Boolean)
    trader = db.Column(db.Boolean)
    text1 = db.Column(db.Text)
    text2 = db.Column(db.Text)
    text3 = db.Column(db.Text)