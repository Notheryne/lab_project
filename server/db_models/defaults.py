from server.db_models.Character import Character
from server.db_models.ItemsInGame import ItemsInGame
from server.db_models.Blueprint import Blueprint
from server.db_models.NonPersonCharacter import NonPersonCharacter
from server.db_models.extensions import db

from copy import deepcopy


default_blueprint_weapon = Blueprint(
    name='Wooden sword',
    price=100,
    slot=0,
    max_health=0,
    strength=0,
    reflex=0,
    charisma=0,
    intelligence=0,
    will=0,
    armor=0,
    min_dmg=2,
    max_dmg=3,
    image_path='https://gamepedia.cursecdn.com/pathofexile_gamepedia/5/53/Ancient_Sword_inventory_icon.png?version=c72ff92bf2321f1540cb22a61e642fbc'
)

default_blueprint_shield = Blueprint(
    name='Wooden shield',
    slot=1,
    price=100,
    max_health=0,
    strength=0,
    reflex=0,
    charisma=0,
    intelligence=0,
    will=0,
    armor=20,
    min_dmg=0,
    max_dmg=0,
    image_path='https://gamepedia.cursecdn.com/pathofexile_gamepedia/9/93/Splintered_Tower_Shield_inventory_icon.png?version=6c41b2174e634dae7be68ef72096378b'
)

default_blueprint_helmet = Blueprint(
    slot=3,
    name='Viking Helmet',
    price=100,
    max_health=10,
    strength=1,
    reflex=0,
    charisma=0,
    intelligence=0,
    will=0,
    armor=0,
    min_dmg=0,
    max_dmg=0,
    image_path='https://gamepedia.cursecdn.com/pathofexile_gamepedia/6/6a/Iron_Hat_inventory_icon.png?version=dd409e0a4ca283e7afbeb5efdf27741e',
)

default_blueprint_armor = Blueprint(
    slot=2,
    name='Leather Armor',
    price=100,
    max_health=10,
    strength=1,
    reflex=0,
    charisma=0,
    intelligence=0,
    will=0,
    armor=0,
    min_dmg=0,
    max_dmg=0,
    image_path='https://gamepedia.cursecdn.com/pathofexile_gamepedia/a/ae/Wild_Leather_inventory_icon.png?version=d2d0f952c8ff390b3a1058a198196dc6',
)

default_blueprint_amulet = Blueprint(
    slot=4,
    name='Basic Talisman',
    price=100,
    max_health=10,
    strength=1,
    reflex=0,
    charisma=0,
    intelligence=0,
    will=0,
    armor=0,
    min_dmg=0,
    max_dmg=0,
    image_path='https://gamepedia.cursecdn.com/pathofexile_gamepedia/4/4a/Hexclaw_Talisman_inventory_icon.png?version=b355d1469b25a9690004c781119cf0b3',
)

default_blueprints = [
    default_blueprint_armor,
    default_blueprint_helmet,
    default_blueprint_amulet,
    default_blueprint_shield,
    default_blueprint_weapon
]

default_healer = NonPersonCharacter(
    name='Akara',
    healer=True,
    trader=False,
    text1="Welcome back, my friend. We are still clearing."
          "the monastery, but you're welcome to stay here as long as you need.",
    text2="Good day. You seem wounded, come and maybe we can fix that.",
    text3="The Order welcomes you. Do you need healing?",
    img_path="https://cdnb.artstation.com/p/assets/images/images/014/413/607/large/greg-mack-akara.jpg?1544499463"
)

default_trader = NonPersonCharacter(
    name='Hephaistos',
    healer=False,
    trader=True,
    text1="Welcome back. Do you need a solid piece of armor?",
    text2="Hi, it's you! I've prepared some special items for my"
          "favourite customer.",
    text3="The Order welcomes you. Your armor seems a little worn out, how about a new one?",
    img_path='http://images6.fanpop.com/image/photos/33400000/Hephaistos-hephaestus-33419337-474-480.jpg'
)

default_npcs = [default_healer, default_trader]


default_char = Character(
    max_health=50,
    health=50,
    level=1,
    experience=0,
    gold=0,
    strength=5,
    reflex=5,
    charisma=5,
    intelligence=5,
    will=5,
    free_stats=0,
    image_path='https://char_placeholder.pl/'
)


def create_default_character(char_name, user_id):
    new_default_char = deepcopy(default_char)
    new_default_char.edit(char_name=char_name, user_id=user_id)

    default_sword = Blueprint.find_by_name('Wooden sword')
    default_sword = {'slot': default_sword.slot, 'blueprint_id': default_sword.id}
    default_shield = Blueprint.find_by_name('Wooden shield')
    default_shield = {'slot': default_shield.slot, 'blueprint_id': default_shield.id}

    return new_default_char, default_sword, default_shield
