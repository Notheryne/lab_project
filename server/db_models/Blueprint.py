from server.db_models.extensions import db


# Slots:
# 0 - weapon
# 1 - shield
# 2 - body armor
# 3 - helmet
# 4 - amulet

class Blueprint(db.Model):
    slots = {
        0: 'weapon',
        1: 'shield',
        2: 'armor',
        3: 'helmet',
        4: 'amulet',
    }

    id = db.Column('id', db.Integer, primary_key=True)
    slot = db.Column(db.Integer, nullable=False)

    name = db.Column('name', db.String(50), nullable=False)
    price = db.Column('price', db.Integer, nullable=False)

    max_health = db.Column('max_health', db.Integer, nullable=False)
    strength = db.Column('strength', db.Integer, nullable=False)
    reflex = db.Column('reflex', db.Integer, nullable=False)
    charisma = db.Column('charisma', db.Integer, nullable=False)
    intelligence = db.Column('intelligence', db.Integer, nullable=False)
    will = db.Column('will', db.Integer, nullable=False)
    armor = db.Column('armor', db.Integer, nullable=False)
    min_dmg = db.Column('min_dmg', db.Integer, nullable=False)
    max_dmg = db.Column('max_dmg', db.Integer, nullable=False)

    image_path = db.Column('img_path', db.String(256), nullable=False)
    items_in_game = db.relationship('ItemsInGame', backref='blueprint')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slot': self.slots[self.slot],
            'price': self.price,
            'max_health': self.max_health,
            'strength': self.strength,
            'reflex': self.reflex,
            'charisma': self.charisma,
            'intelligence': self.intelligence,
            'will': self.will,
            'armor': self.armor,
            'min_dmg': self.min_dmg,
            'max_dmg': self.max_dmg,
            'img_path': self.image_path,
            'iig': self.items_in_game,
        }

    def to_dict_stats(self):
        return {
            'name': self.name,
            'slot': self.slots[self.slot],
            'image_path': self.image_path,
            'max_health': self.max_health,
            'strength': self.strength,
            'reflex': self.reflex,
            'charisma': self.charisma,
            'intelligence': self.intelligence,
            'will': self.will,
            'armor': self.armor,
            'min_dmg': self.min_dmg,
            'max_dmg': self.max_dmg,
        }

    @classmethod
    def find_by_id(cls, bp_id):
        return cls.query.filter_by(id=bp_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
