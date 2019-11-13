import requests
import random


def populate(users=10, items=10, blueprints=10, enemies=10):
    basic_url = 'http://localhost:5000/'
    register_ep = 'register'
    login_ep = 'login'
    blueprint_ep = 'add/blueprint'
    items_ep = 'add/item'
    enemy_ep = 'add/enemy'

    # Register
    for i in range(users):
        data = {
            'username': 'User' + str(i),
            'password': 123,
            'email': 'user{}@user.pl'.format(str(i)),
            'char_name': 'Char' + str(i),
        }
        requests.post(basic_url + register_ep, data=data)

    # Get token
    data = {'username': 'User1', 'password': 123}
    token = requests.post(basic_url + login_ep, data=data).json()['access_token']

    headers = {'Authorization': 'Bearer {}'.format(token)}

    # Add random blueprints
    for i in range(blueprints):
        slot = random.randint(1, 6)
        data = {
            'slot': slot,
            'name': 'Blueprint ' + str(slot),
            'price': random.randint(10, 1000),
            'health': random.randint(0, 50),
            'strength': random.randint(0, 20),
            'reflex': random.randint(0, 20),
            'charisma': random.randint(0, 20),
            'intelligence': random.randint(0, 20),
            'will': random.randint(0, 20),
            'armor': random.randint(0, 20),
            'min_dmg': random.randint(0, 20),
            'max_dmg': random.randint(20, 40),
            'image_path': 'http://img_placeholder.xd',
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


populate()


