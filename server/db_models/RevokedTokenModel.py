from server.db_models.extensions import db


class RevokedTokenModel(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    jti = db.Column('jti', db.String(120))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
