from server.db_models.extensions import db


class Enemy(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('enemy_name', db.String(35), unique=True, nullable=False)
    experience = db.Column('experience', db.Integer, nullable=False)
    gold = db.Column('gold', db.Integer, nullable=False)

    health = db.Column('health', db.Integer, nullable=False)
    strength = db.Column('strength', db.Integer, nullable=False)
    reflex = db.Column('reflex', db.Integer, nullable=False)
    charisma = db.Column('charisma', db.Integer, nullable=False)
    intelligence = db.Column('intelligence', db.Integer, nullable=False)
    will = db.Column('will', db.Integer, nullable=False)

    armor = db.Column('armor', db.Integer, nullable=False)
    min_dmg = db.Column('minimal_dmg', db.Integer, nullable=False)
    max_dmg = db.Column('maximal_dmg', db.Integer, nullable=False)

    image_path = db.Column('image_path', db.String(256), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'experience': self.experience,
            'gold': self.gold,
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