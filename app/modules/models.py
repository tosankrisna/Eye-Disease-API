from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class EyeDisease(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(25))
    img_url = db.Column(db.String(100))
    desc = db.Column(db.String(100))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'img_url': self.img_url,
            'desc': self.img_url
        }