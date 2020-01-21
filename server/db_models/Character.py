from server.db_models.extensions import db
from sqlalchemy.exc import IntegrityError


class Character(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('char_name', db.String(45), unique=True, nullable=False)

    level = db.Column('level', db.Integer, nullable=False)
    experience = db.Column('experience', db.Integer, nullable=False)
    gold = db.Column('money', db.Integer, nullable=False)

    max_health = db.Column('max_health', db.Integer, nullable=False)
    health = db.Column('health', db.Integer, nullable=False)
    strength = db.Column('strength', db.Integer, nullable=False)
    reflex = db.Column('reflex', db.Integer, nullable=False)
    charisma = db.Column('charisma', db.Integer, nullable=False)
    intelligence = db.Column('intelligence', db.Integer, nullable=False)
    will = db.Column('will', db.Integer, nullable=False)
    free_stats = db.Column('free_stats', db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    itemsingame = db.relationship('ItemsInGame', backref='character', lazy=True)

    image_path = db.Column('img_path', db.String(256), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'experience': self.experience,
            'gold': self.gold,
            'max_health': self.max_health,
            'health': self.health,
            'strength': self.strength,
            'reflex': self.reflex,
            'charisma': self.charisma,
            'intelligence': self.intelligence,
            'will': self.will,
            'free_stats': self.free_stats,
            'user_id': self.user_id,
            'items_in_game': self.itemsingame,
            'image_path': self.image_path
        }

    def to_dict_stats(self):
        return {
            'max_health': self.max_health,
            'health': self.health,
            'strength': self.strength,
            'reflex': self.reflex,
            'charisma': self.charisma,
            'intelligence': self.intelligence,
            'will': self.will,
            'items_in_game': self.itemsingame,
        }

    def add_stat(self, stat=''):
        if self.free_stats > 0:
            if stat == 'strength':
                self.strength += 1
            elif stat == 'reflex':
                self.reflex += 1
            elif stat == 'charisma':
                self.charisma += 1
            elif stat == 'intelligence':
                self.intelligence += 1
            elif stat == 'will':
                self.will += 1
            self.free_stats -= 1
            return {'success': True, 'increased': stat, 'increased_by': 1}
        else:
            return {'success': False, 'message': 'Not enough free stats.'}

    def set_character_name(self, new_name):
        if len(new_name) == 0:
            return {'success': False, 'message': 'Username cannot be empty.'}
        elif len(new_name) < 4:
            return {'success': False, 'message': 'Username too short.'}
        self.name = new_name
        try:
            self.save()
        except IntegrityError:
            return {'success': False, 'message': 'This username is already taken.'}, 400
        return {'success': True, 'message': 'New username set. Remember to login using "{0}".'.format(new_name)}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id, todict=False):
        if todict:
            return cls.query.filter_by(id=id).first().to_dict()
        else:
            return cls.query.filter_by(id=id).first()

    def edit(self, char_name=None, user_id=None, health=None, level=None, experience=None, gold=None,
             free_stats=None):
        if char_name:
            self.name = char_name
        if user_id:
            self.user_id = user_id
        if health:
            self.health = health
        if level:
            self.level = level
        if experience:
            self.experience = experience
        if gold:
            self.gold += gold
        if free_stats:
            self.free_stats += free_stats

    def save(self):
        db.session.add(self)
        db.session.commit()

