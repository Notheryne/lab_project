from server.db_models.extensions import db


class NonPersonCharacter(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('npc_name', db.String(35), unique=True, nullable=False)
    healer = db.Column('healer', db.Boolean)
    trader = db.Column('trader', db.Boolean)
    text1 = db.Column('text_line1', db.Text)
    text2 = db.Column('text_line2', db.Text)
    text3 = db.Column('text_line3', db.Text)
    img_path = db.Column('image_path', db.String(256), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'healer': self.healer,
            'trader': self.trader,
            'texts': [self.text1, self.text2, self.text3],
            'img_path': self.img_path,
        }

    @classmethod
    def find_by_name(cls, npc_name):
        return cls.query.filter_by(name=npc_name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
