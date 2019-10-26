from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    name = db.Column(db.String(35), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    create_date = db.Column('create_date', db.DateTime, default=datetime.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Character(db.Model):
    char_id = db.Column('char_id', db.Integer, primary_key=True)
    char_name = db.Column('', unique=True, nullable=False)

    health = db.Column('')
    strength = db.Column('')
    reflex = db.Column('')
    charisma = db.Column('')
    intelligence = db.Column('')
    will = db.Column('')

    user = db.Column('', unique=True, nullable=False)
    image_path = db.Column('')


class Blueprints(db.Model):
    bp_id = db.Column('bp_id', db.Integer, primary_key=True)
    bp_type = db.Column('')

    health = db.Column('')
    strength = db.Column('')
    reflex = db.Column('')
    charisma = db.Column('')
    intelligence = db.Column('')
    will = db.Column('')
    armor = db.Column('')
    min_dmg = db.Column('')
    max_dmg = db.Column('')

    image_path = db.Column('')


class ItemsInGame(db.Model):
    iig_id = db.Column('iig_id', db.Integer, primary_key=True)
    slot = db.Column('')
    name = db.Column('')
    equipped = db.Column('')
    blueprint = db.Column('')
    character = db.Column('')


class Enemy(db.Model):
    enemy_id = db.Column('enemy_id', db.Integer, primary_key=True)
    name = db.Column('', unique=True, nullable=False)
    rarity = db.Column('')
    health = db.Column('')
    strength = db.Column('')
    reflex = db.Column('')
    charisma = db.Column('')
    intelligence = db.Column('')
    will = db.Column('')

    armor = db.Column('')
    min_dmg = db.Column('')
    max_dmg = db.Column('')

    image_path = db.Column('')


class NonPersonCharacter(db.Model):
    npc_id = db.Column('npc_id', db.Integer, primary_key=True)
    name = db.Column('', unique=True, nullable=False)
    healer = db.Column('')
    trader = db.Column('')
    text1 = db.Column('')
    text2 = db.Column('')
    text3 = db.Column('')