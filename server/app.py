from flask import Flask, jsonify, request, redirect, g, make_response
from server.db_models.models import *
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin
import jwt

login_site_path = 'front/main_page/index.html'

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://game_admin:#dmiN123@localhost/game'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

auth = HTTPBasicAuth()

with app.app_context():
    db.init_app(app)
    db.drop_all(app=app)
    db.create_all(app=app)

    u = User(name='Nothy', email='nothy@nothy.com', password='123456')
    db.session.add(u)
    db.session.commit()
    c = Character(char_name="Nothy", health=20, strength=20, reflex=20,
                  charisma=20, intelligence=20, will=20, user_id=1,
                  image_path='https://upload.wikimedia.org/wikipedia/en/thumb/6/63/IMG_%28business%29.svg/1200px-IMG_%28business%29.svg.png')
    db.session.add(c)
    db.session.commit()


@app.route('/api/users', methods=['OPTIONS', 'GET', 'POST'])
@cross_origin()
def handle():
    if request.method == "POST":
        data = request.json
        print(data)
        response = {
            'success': True,
            'goto': 'index.html',
        }
        response = jsonify(response)
        # response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    elif request.method == "GET":
        return 'Ok'



@app.route ('/character/<char_id>', methods=['GET'])
@auth.login_required
def get_character(char_id):
    data = Character.query.get(int(char_id)).__dict__
    del data['_sa_instance_state']
    print(data)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
