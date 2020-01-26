from server.db_models.extensions import db


class ItemsInGame(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    slot = db.Column('slot', db.Integer, nullable=False)
    blueprint_id = db.Column('blueprint_id', db.Integer, db.ForeignKey('blueprint.id'))
    character_id = db.Column('character_id', db.Integer, db.ForeignKey('character.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'slot': self.slot,
            'bp_id': self.blueprint_id,
            'char_id': self.character_id,
        }

    def edit(self, char_id=0):
        self.character_id = char_id

    def save(self):
        db.session.add(self)
        db.session.commit()