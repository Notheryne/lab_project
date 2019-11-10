import requests


register = 'http://localhost:5000/r'
login = 'http://localhost:5000/l'
register_data1 = {
    'username': 'Nothy',
    'password': '123',
    'email': 'a@a.a',
    'char_name': 'Nothy'
}
register_data2 = {
    'username': 'Nothy2',
    'password': '123',
    'email': 'a2@a.a',
    'char_name': 'Nothy2'
}
register_data3 = {
    'username': 'Nothy3',
    'password': '123',
    'email': 'a3@a.a',
    'char_name': 'Nothy3'
}

requests.post(register, data=register_data1).json()
requests.post(register, data=register_data2).json()
requests.post(register, data=register_data3).json()

login_data = {
    'username': 'Nothy',
    'password': '123'
}

token = requests.post(login, data=login_data).json()['access_token']

fight = 'http://localhost:5000/fight'
fight_data = {
    'attacker_id': 1,
    'defender_id': 2
}
fight_header = {
    'Authorization': 'Bearer {}'.format(token)
}

f = requests.post(fight, data=fight_data, headers=fight_header)
print(f.json())
