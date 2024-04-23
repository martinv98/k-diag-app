from app import db


class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
