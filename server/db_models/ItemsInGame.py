from server.db_models.db import db


class ItemsInGame(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    slot = db.Column('slot', db.Integer, nullable=False)
    equipped = db.Column('equipped', db.Boolean)
    blueprint_id = db.Column('bp_id', db.Integer, db.ForeignKey('blueprint.id'))
    character_id = db.Column('char_id', db.Integer, db.ForeignKey('character.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'slot': self.slot,
            'equipped': self.equipped,
            'bp_id': self.blueprint_id,
            'char_id': self.character_id,
        }

    def edit(self, char_id=0, blueprint_id=0):
        self.character_id = char_id
