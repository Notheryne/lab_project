from server.db_models.db import db


class NonPersonCharacter(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('npc_name', db.String(35), unique=True, nullable=False)
    healer = db.Column(db.Boolean)
    trader = db.Column(db.Boolean)
    text1 = db.Column(db.Text)
    text2 = db.Column(db.Text)
    text3 = db.Column(db.Text)
    image_path = db.Column('img_path', db.String(256), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
