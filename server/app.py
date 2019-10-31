from flask import Flask
from server.db_models.models import *


app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://game_admin:#dmiN123@localhost/game'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
db.drop_all(app=app)
db.create_all(app=app)


@app.route('/')
def hello_world():
    print(db.desc('user'))
    return 'hello_world'


if __name__ == '__main__':
    app.run()
