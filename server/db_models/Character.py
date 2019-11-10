from server.db_models.db import db


class Character(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('char_name', db.String(45), unique=True, nullable=False)

    level = db.Column('level', db.Integer, nullable=False)
    experience = db.Column('experience', db.Integer, nullable=False)
    health = db.Column('health', db.Integer, nullable=False)
    strength = db.Column('strength', db.Integer, nullable=False)
    reflex = db.Column('reflex', db.Integer, nullable=False)
    charisma = db.Column('charisma', db.Integer, nullable=False)
    intelligence = db.Column('intelligence', db.Integer, nullable=False)
    will = db.Column('will', db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    itemsingame = db.relationship('ItemsInGame', backref='character', lazy=True)

    image_path = db.Column('img_path', db.String(256), nullable=False)

    def __repr__(self):
        return 'id: {}, char_name: {}, level: {}, experience: {}, health: {}, strength: {}, reflex: {}, ' \
               'charisma: {}, intelligence: {}, will: {}, user_id: {}, itemsingame: {}, image_path:{}'.format(
                self.id, self.char_name, self.level, self.experience, self.health, self.strength, self.reflex,
                self.charisma,
                self.intelligence, self.will, self.user_id, self.itemsingame, self.image_path
                )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'experience': self.experience,
            'health': self.health,
            'strength': self.strength,
            'reflex': self.reflex,
            'charisma': self.charisma,
            'intelligence': self.intelligence,
            'will': self.will,
            'user_id': self.user_id,
            'items_in_game': self.itemsingame,
            'image_path': self.image_path
        }

    def to_dict_stats(self):
        return {
            'health': self.health,
            'strength': self.strength,
            'reflex': self.reflex,
            'charisma': self.charisma,
            'intelligence': self.intelligence,
            'will': self.will,
            'items_in_game': self.itemsingame,
        }

    @classmethod
    def find_character_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def edit(self, char_name='', user_id='', health=0):
        if char_name != '':
            self.name = char_name
        if user_id != '':
            self.user_id = user_id
        if health != 0:
            self.health = health
