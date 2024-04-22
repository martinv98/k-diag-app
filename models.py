from app import db


class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)