from server.db_models.db import db


class RevokedTokenModel(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
