from server.db_models.Character import Character
from server.db_models.ItemsInGame import ItemsInGame
from server.db_models.Blueprint import Blueprint
from server.db_models.db import db

from copy import deepcopy
default_blueprint_weapon = Blueprint(
    name='Wooden sword',
    type=0,
    health=0,
    strength=0,
    reflex=0,
    charisma=0,
    intelligence=0,
    will=0,
    armor=0,
    min_dmg=2,
    max_dmg=3,
    image_path='https://gamepedia.cursecdn.com/arksurvivalevolved_gamepedia/8/89/Sword.png'
)

default_blueprint_shield = Blueprint(
    name='Wooden shield',
    type=1,
    health=0,
    strength=0,
    reflex=0,
    charisma=0,
    intelligence=0,
    will=0,
    armor=20,
    min_dmg=0,
    max_dmg=0,
    image_path='https://gamepedia.cursecdn.com/arksurvivalevolved_gamepedia/8/89/Sword.png'
)


default_weapon = ItemsInGame(
    slot=0,
    equipped=True,
    blueprint_id=1,
)

default_shield = ItemsInGame(
    slot=1,
    equipped=True,
    blueprint_id=2,
)


default_char = Character(
    health=50,
    level=1,
    experience=0,
    strength=5,
    reflex=5,
    charisma=5,
    intelligence=5,
    will=5,
    image_path='https://pbs.twimg.com/profile_images/600781122688122880/ZZgzd0UC.jpg'
)


def create_default_character(char_name, user_id):
    new_default_char = deepcopy(default_char)
    new_default_char.edit(char_name, user_id)
    db.session.add(new_default_char)
    db.session.commit()
    char_id = new_default_char.id

    new_default_weapon = deepcopy(default_weapon)
    new_default_shield = deepcopy(default_shield)
    new_default_weapon.edit(char_id=char_id)
    new_default_shield.edit(char_id=char_id)
    db.session.add(new_default_weapon)
    db.session.add(new_default_shield)
    db.session.commit()

