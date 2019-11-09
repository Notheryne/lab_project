from server.db_models.db import db


class Enemy(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('enemy_name', db.String(35), unique=True, nullable=False)
    rarity = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Integer, nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    reflex = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    will = db.Column(db.Integer, nullable=False)

    armor = db.Column(db.Integer, nullable=False)
    min_dmg = db.Column(db.Integer, nullable=False)
    max_dmg = db.Column(db.Integer, nullable=False)

    image_path = db.Column('img_path', db.String(256), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()