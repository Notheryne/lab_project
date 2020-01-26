import requests
from bs4 import BeautifulSoup
import pickle
from random import randint, choice
import urllib.parse

from server.db_models.Character import Character
from server.db_models.ItemsInGame import ItemsInGame
from server.db_models.Blueprint import Blueprint
from server.db_models.Enemy import Enemy
from server.db_models.User import User
from server.db_models.defaults import *
from server.db_models.extensions import db
from sqlalchemy.exc import IntegrityError
SLOTS = {
    0: 'weapon',
    1: 'shield',
    2: 'armor',
    3: 'helmet',
    4: 'amulet',
}

base_url = 'http://localhost:5000/'
register_ep = 'api/register'
login_ep = 'api/login'
blueprint_ep = 'api/add/blueprint'
items_ep = 'api/add/item'
enemy_ep = 'api/add/enemy'


def get_image_paths(get_new_icons):
    images_urls = {
        'armor': 'https://pathofexile.gamepedia.com/Category:Body_armour_icons',
        'amulet': 'https://pathofexile.gamepedia.com/Category:Amulet_icons',
        'sceptre': 'https://pathofexile.gamepedia.com/Category:Sceptre_icons',
        'sword': 'https://pathofexile.gamepedia.com/Category:Sword_icons',
        'shield': 'https://pathofexile.gamepedia.com/Category:Shield_icons',
        'helmet': 'https://pathofexile.gamepedia.com/Category:Helmet_icons',
        'enemy': 'https://pathofexile.gamepedia.com/Category:Monster_screenshots',
    }

    images = {'weapon': []}

    if get_new_icons:
        for category, url in images_urls.items():
            page = requests.get(url).text
            soup = BeautifulSoup(page, 'html.parser')
            soup = soup.find_all('img')
            category_images = []
            for path in soup:
                if 'gamepedia' in path['src']:
                    category_images.append(path['src'])
            if category in ['sceptre', 'sword']:
                images['weapon'] += category_images
            else:
                images[category] = category_images

        pickle.dump(images, open('db_models/images.pickle', 'wb'))
    else:
        images = pickle.load(open('db_models/images.pickle', 'rb'))
    return images


def add_users(users):
    for i in range(users):
        name = 'User' + str(i)
        email = 'user{}@gmail.com' + str(i)
        password = '123'
        u = User(name, email, password)
        u.save()
        new_char, default_sword, default_shield = create_default_character(name, u.id)
        new_char.save()

        ItemsInGame(**default_sword, character_id=new_char.id).save()
        ItemsInGame(**default_shield, character_id=new_char.id).save()
        print("Created user ", i)


def get_name(image_path, remove=None):
    name = image_path.split('?')[0]
    name = name.rsplit('/', 2)[-1]
    name = name.split('-')[-1]
    if remove:
        name = name[:-len(remove)]
    name = urllib.parse.unquote(name)
    name = name.replace('_', ' ').replace('race', '')
    name = name.replace('season', '').replace('emberwake', '')
    for i in range(9):
        name = name.replace(str(i), '')
    name = name.strip()
    return name


def get_stats(slot=10, enemy=False):
    max_health = randint(0, 150) if randint(0, 10) > 3 else 0
    strength = randint(0, 100) if randint(0, 10) > 7 else 0
    reflex = randint(0, 100) if randint(0, 10) > 7 else 0
    charisma = randint(0, 100) if randint(0, 10) > 7 else 0
    intelligence = randint(0, 100) if randint(0, 10) > 7 else 0
    will = randint(0, 100) if randint(0, 10) > 7 else 0
    min_dmg = randint(0, 100) if slot == 0 or enemy else 0
    max_dmg = min_dmg + randint(0, 40) if slot == 0 or enemy else 0
    armor = randint(0, 1000) if 0 < slot < 4 or enemy else 0
    stats = [max_health, strength, reflex, charisma,
             intelligence, will, min_dmg, max_dmg, armor]
    return (max_health, strength, reflex, charisma, intelligence,
            will, min_dmg, max_dmg, armor, stats)


def add_blueprints(items, images):
    for i in range(items):
        slot = randint(0, 4)
        slot_name = SLOTS[slot]
        image_path = choice(images[slot_name])
        item_name = get_name(image_path, '_inventory_icon.png')
        (max_health, strength, reflex, charisma, intelligence, will,
            min_dmg, max_dmg, armor, stats) = get_stats(slot)
        price = sum(stats) + randint(100, 1000)
        bp = Blueprint(
            slot=slot,
            name=item_name,
            price=price,
            max_health=max_health,
            strength=strength,
            reflex=reflex,
            charisma=charisma,
            intelligence=intelligence,
            will=will,
            armor=armor,
            min_dmg=min_dmg,
            max_dmg=max_dmg,
            image_path=image_path
        )
        try:
            bp.save()
        except IntegrityError:
            bp.name = 'item_name' + str(randint(0, 50))
        print("Created bp", i)


def add_enemies(enemies, images):
    for i in range(enemies):
        image_path = choice(images)

        name = get_name(image_path, '.jpg')
        (health, strength, reflex, charisma, intelligence, will,
            min_dmg, max_dmg, armor, stats) = get_stats()

        experience = sum(stats) + randint(50, 700)
        gold = sum(stats) + randint(50, 200)
        e = Enemy(
            name=name,
            experience=experience,
            gold=gold,
            health=health,
            strength=strength,
            reflex=reflex,
            charisma=charisma,
            intelligence=intelligence,
            will=will,
            armor=armor,
            min_dmg=min_dmg,
            max_dmg=max_dmg,
            image_path=image_path
        )
        try:
            e.save()
        except IntegrityError:
            db.session.rollback()
            e.name = name + str(randint(0, 50))
            e.save()
        print("Created enemy", i)


def give_items(give_items_to):
    characters = Character.query.all()
    items = Blueprint.query.all()
    for i in range(give_items_to):
        char = choice(characters)
        item = choice(items)
        iig = ItemsInGame(slot=item.slot, blueprint_id=item.id, character_id=char.id)
        try:
            db.session.rollback()
            iig.save()
        except IntegrityError:
            continue


def populate(users, items, enemies, give_items_to):
    images = get_image_paths(False)
    if users:
        add_users(users)

    add_blueprints(items, images)
    add_enemies(enemies, images['enemy'])
    give_items(give_items_to)
    print(users, items, enemies, give_items_to)


if __name__ == "__main__":
    populate()
