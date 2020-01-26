import requests
import random


def populate(users=10, items=10, blueprints=10, enemies=10):
    basic_url = 'http://localhost:5000/'
    register_ep = 'api/register'
    login_ep = 'api/login'
    blueprint_ep = 'api/add/blueprint'
    items_ep = 'api/add/item'
    enemy_ep = 'api/add/enemy'

    # # Register
    # for i in range(users):
    #     data = {
    #         'username': 'User' + str(i),
    #         'password': 123,
    #         'email': 'user{}@user.pl'.format(str(i)),
    #         'char_name': 'Char' + str(i),
    #     }
    #     requests.post(basic_url + register_ep, data=data)
    #
    # # Get token
    # data = {'username': 'User1', 'password': 123}
    data = {'username': 'User', 'password': 123}
    token = requests.post(basic_url + login_ep, data=data).json()['access_token']

    headers = {'Authorization': 'Bearer {}'.format(token)}

    images = {
        'helmet': 'https://gamepedia.cursecdn.com/pathofexile_gamepedia/6/6a/Iron_Hat_inventory_icon.png?version=dd409e0a4ca283e7afbeb5efdf27741e',
        'amulet': 'https://gamepedia.cursecdn.com/pathofexile_gamepedia/4/4a/Hexclaw_Talisman_inventory_icon.png?version=b355d1469b25a9690004c781119cf0b3',
        'armor': 'https://gamepedia.cursecdn.com/pathofexile_gamepedia/a/ae/Wild_Leather_inventory_icon.png?version=d2d0f952c8ff390b3a1058a198196dc6',
        'weapon': 'https://gamepedia.cursecdn.com/pathofexile_gamepedia/5/53/Ancient_Sword_inventory_icon.png?version=c72ff92bf2321f1540cb22a61e642fbc',
        'shield': 'https://gamepedia.cursecdn.com/pathofexile_gamepedia/9/93/Splintered_Tower_Shield_inventory_icon.png?version=6c41b2174e634dae7be68ef72096378b',
    }
    slots = {
        0: 'weapon',
        1: 'shield',
        2: 'armor',
        3: 'helmet',
        4: 'amulet',
    }
    # Add random blueprints
    for i in range(blueprints):
        slot = random.randint(0, 4)
        data = {
            'slot': slot,
            'name': 'Blueprint ' + str(slot),
            'price': random.randint(10, 1000),
            'max_health': random.randint(0, 50),
            'strength': random.randint(0, 20),
            'reflex': random.randint(0, 20),
            'charisma': random.randint(0, 20),
            'intelligence': random.randint(0, 20),
            'will': random.randint(0, 20),
            'armor': random.randint(0, 20),
            'min_dmg': random.randint(0, 20),
            'max_dmg': random.randint(20, 40),
            'image_path': images[slots[slot]],
        }
        requests.post(basic_url + blueprint_ep, data=data, headers=headers)

    # Add random items
    for i in range(items):
        data = {
            'blueprint_id': random.randint(1, blueprints),
            'character_id': random.randint(1, users)
        }
        requests.post(basic_url + items_ep, data=data, headers=headers)

    # Add random enemies
    for i in range(enemies):
        data = {
            'name': 'Enemy' + str(i),
            'experience': random.randint(100, 1000),
            'gold': random.randint(100, 1000),
            'health': random.randint(20, 1000),
            'strength': random.randint(1, 50),
            'reflex': random.randint(1, 50),
            'charisma': random.randint(1, 50),
            'intelligence': random.randint(1, 50),
            'will': random.randint(1, 50),
            'armor': random.randint(1, 50),
            'min_dmg': random.randint(1, 30),
            'max_dmg': random.randint(30, 50),
            'image_path': 'https://enemy_placeholder.pl',
        }
        requests.post(basic_url + enemy_ep, data=data, headers=headers)




