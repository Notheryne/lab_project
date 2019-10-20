from peewee import *
from peewee_extra_fields import SimplePasswordField
import datetime
import secrets
import uuid
import logging

db = MySQLDatabase(
    database='game',
    user='game_admin',
    password='@dmiN123',
    charset='utf8'
)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    username = CharField(unique=True)
    password = SimplePasswordField(salt=secrets.token_urlsafe(), min_length=6)
    create_date = DateTimeField(default=datetime.datetime.now())


class Character(BaseModel):
    char_id = IntegerField(default=0, unique=True, primary_key=True)
    char_name = CharField(max_length=35, unique=True)

    base_health = IntegerField()
    base_strength = IntegerField()
    base_reflex = IntegerField()
    base_charisma = IntegerField()
    base_intelligence = IntegerField()
    base_will = IntegerField()
    user = ForeignKeyField(User, backref='character')

    image_path = CharField(max_length=1024)


class Blueprints(BaseModel):
    bp_id = PrimaryKeyField()
    type = IntegerField()
    health = IntegerField()
    strength = IntegerField()
    reflex = IntegerField()
    charisma = IntegerField()
    intelligence = IntegerField()
    will = IntegerField()

    armor = IntegerField()
    min_dmg = IntegerField()
    max_dmg = IntegerField()

    image_path = CharField(max_length=1024)


class ItemsInGame(BaseModel):
    iig_id = PrimaryKeyField()
    item_slot = IntegerField()
    item_name = CharField(max_length=45)
    equipped = BooleanField()
    blueprint = ForeignKeyField(Blueprints, backref='owned_items')
    character = ForeignKeyField(Character, backref='owned_items')


class Enemy(BaseModel):
    enemy_id = PrimaryKeyField()
    name = CharField(50)
    rarity = IntegerField()
    health = IntegerField()
    strength = IntegerField()
    reflex = IntegerField()
    charisma = IntegerField()
    intelligence = IntegerField()
    will = IntegerField()

    armor = IntegerField()
    min_dmg = IntegerField()
    max_dmg = IntegerField()

    image_path = CharField(max_length=1024)


class NonPersonCharacter(BaseModel):
    npc_id = PrimaryKeyField()
    name = CharField(50)
    healer = BooleanField()
    trader = BooleanField()
    text1 = TextField()
    text2 = TextField()
    text3 = TextField()
