from flask import Flask
from db_models.models import *


app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://game_admin:@dmiN123@localhost/game'
db.init_app(app)
# if __name__ == '__main__':
#     app.run()
