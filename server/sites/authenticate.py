from flask import Blueprint
from flask_login import
login = Blueprint('login', __name__)

@login.route('/login')
def login():
