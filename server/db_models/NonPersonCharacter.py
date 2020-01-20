from server.db_models.extensions import db


class NonPersonCharacter(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('npc_name', db.String(35), unique=True, nullable=False)
    healer = db.Column('healer', db.Boolean)
    trader = db.Column('trader', db.Boolean)
    text1 = db.Column('text1', db.Text)
    text2 = db.Column('text2', db.Text)
    text3 = db.Column('text3', db.Text)
    img_path = db.Column('img_path', db.String(256), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'healer': self.healer,
            'trader': self.trader,
            'texts': [self.text1, self.text2, self.text3],
            'img_path': self.img_path,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
