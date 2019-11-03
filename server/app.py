from flask import Flask, jsonify, request
from server.db_models.models import *
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://game_admin:#dmiN123@localhost/game'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app)
login = LoginManager(app)
with app.app_context():
    db.init_app(app)
    db.drop_all(app=app)
    db.create_all(app=app)

    u = User(name='Nothy', email='nothy@nothy.com')
    u.set_password('123456')
    db.session.add(u)
    db.session.commit()
    c = Character(char_name="Nothy", health=20, strength=20, reflex=20,
                  charisma=20, intelligence=20, will=20, user_id=1,
                  image_path='https://upload.wikimedia.org/wikipedia/en/thumb/6/63/IMG_%28business%29.svg/1200px-IMG_%28business%29.svg.png')
    db.session.add(c)
    db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        print(request.json)
    data = {
        'success': True,
        'goto_url': 'http://127.0.0.1:5000/login',
    }
    return jsonify(data)


@app.route ('/character/<char_id>', methods=['GET'])
def get_character(char_id):
    data = Character.query.get(int(char_id)).__dict__
    del data['_sa_instance_state']
    print(data)
    return jsonify(data)


if __name__ == '__main__':
    app.run()
