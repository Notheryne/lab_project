from server.db_models.db import db


class Enemy(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('enemy_name', db.String(35), unique=True, nullable=False)
    experience = db.Column(db.Integer, nullable=False)

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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'rarity': self.rarity,
            'experience': self.experience,
            'health': self.health,
            'strength': self.strength,
            'reflex': self.reflex,
            'charisma': self.charisma,
            'intelligence': self.intelligence,
            'will': self.will,
            'armor': self.armor,
            'min_dmg': self.min_dmg,
            'max_dmg': self.max_dmg,
            'image_path': self.image_path,
        }

    def to_dict_stats(self):
        return {
            'experience': self.experience,
            'health': self.health,
            'strength': self.strength,
            'reflex': self.reflex,
            'charisma': self.charisma,
            'intelligence': self.intelligence,
            'will': self.will,
            'armor': self.armor,
            'min_dmg': self.min_dmg,
            'max_dmg': self.max_dmg,
        }
    def save(self):
        db.session.add(self)
        db.session.commit()