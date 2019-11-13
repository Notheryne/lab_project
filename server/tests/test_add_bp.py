import requests
import random
register = 'http://localhost:5000/r'

data = {'username': 'Nothy', 'password': 123, 'email': 'email@email.com', 'char_name': 'Nothy'}

requests.post(register, data=data)

login = 'http://localhost:5000/l'

data = {'username': 'Nothy', 'password': 123}
token = str(requests.post(login, data=data).json()['access_token'])

headers = {'Authorization': 'Bearer {}'.format(token)}

blueprint = 'http://localhost:5000/add/blueprint'
slot = random.randint(1, 6)
data = {
    'slot': slot,
    'name': 'Blueprint ' + str(slot),
    'price': 100,
    'health': 50,
    'strength': 2,
    'reflex': 2,
    'charisma': 2,
    'intelligence': 2,
    'will': 2,
    'armor': 2,
    'min_dmg': 2,
    'max_dmg': 2,
    'image_path': 'http',
}

r = requests.post(blueprint, data=data, headers=headers)

print(r.json())