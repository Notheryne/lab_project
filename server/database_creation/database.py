from peewee import *
from peewee_extra_fields import SimplePasswordField
import datetime
import secrets

db = MySQLDatabase('a.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(Model):
    user_id = UUIDField(unique=True, primary_key=True)
    username = CharField(unique=True)
    password = SimplePasswordField(salt=secrets.token_urlsafe(), min_length=6)
    create_date = DateTimeField(datetime.datetime.now())


class Character(Model):
    char_id = PrimaryKeyField()
    char_name = CharField(max_length=35, unique=True)

    base_health = IntegerField()
    base_strength = IntegerField()
    base_reflex = IntegerField()
    base_charisma = IntegerField()
    base_intelligence = IntegerField()
    base_will = IntegerField()

    # TODO: Bonus stats as foreign keys from items_in_game
    # TODO: armor, min_dmg, max_dmg

    health = IntegerField()
    strength = IntegerField()
    reflex = IntegerField()
    charisma = IntegerField()
    intelligence = IntegerField()
    will = IntegerField()


class ItemsInGame(Model):
    iig_id = PrimaryKeyField()
    item_slot = IntegerField()
    item_name = CharField(max_length=30)
    equipped = BooleanField()

class Blueprints(Model):
    bp_id = PrimaryKeyField()
    bp_type = IntegerField()
    health = IntegerField()
    strength = IntegerField()
    reflex = IntegerField()
    charisma = IntegerField()
    will = IntegerField()

    armor = IntegerField()
    min_dmg = IntegerField()
    max_dmg = IntegerField()

