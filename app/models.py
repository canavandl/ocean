from app import db


class Spectrum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wavelengths = db.Column(db.String, index=True)
    values = db.Column(db.String, index=True)

    def __repr__(self):
        return '<id %r>' % (self.id)