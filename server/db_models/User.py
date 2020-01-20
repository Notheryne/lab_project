from server.db_models.extensions import db

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(60), unique=True, nullable=False)
    name = db.Column('user_name', db.String(35), unique=True, nullable=False)
    password_hash = db.Column('password_hash', db.String(128))
    create_date = db.Column('create_date', db.DateTime)
    character = db.relationship('Character', backref='user', lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)
        self.create_date = datetime.now()

    def to_dict(self):
        return {
            'id': {'value': self.id, 'changeable': False},
            'email': {'value': self.email, 'changeable': False},
            'name': {'value': self.name, 'changeable': False},
            'create_date': {'value': self.create_date, 'changeable': False},
            'character': {'value': self.character, 'changeable': False},
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_user_by_name(cls, username):
        return cls.query.filter_by(name=username).first()

    @classmethod
    def find_user_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id
