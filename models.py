from app import db


class User(db.Model):
    __tablename__ = 'user'
    userId = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password.decode('utf-8')
        }


class CTScan(db.Model):
    __tablename__ = 'ctscan'
    ctId = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    filename = db.Column(db.String(80), nullable=True)
    metadataCT = db.Column(db.String(10000), nullable=True)

    def to_dict(self):
        return {
            'filename': self.filename,
            'metadataCT': self.metadataCT
        }


class Mask(db.Model):
    __tablename__ = 'mask'
    maskId = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    filename = db.Column(db.String(80), nullable=True)
    metadataMask = db.Column(db.String(10000), nullable=True)

    def to_dict(self):
        return {
            'filename': self.filename,
            'metadataMask': self.metadataMask
        }


class Instance(db.Model):
    __tablename__ = 'instance'
    instanceId = db.Column(db.Integer, unique=True, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'), nullable=True)
    ctId = db.Column(db.Integer, db.ForeignKey('ctscan.ctId'), nullable=True)
    maskId = db.Column(db.Integer, db.ForeignKey('mask.maskId'), nullable=True)
    result = db.Column(db.Boolean, nullable=True)
    resultAccuracy = db.Column(db.Float, nullable=True)
    resultString = db.Column(db.String(10000), nullable=True)
    user = db.relationship('User', backref=db.backref('instance', lazy=True))

    def to_dict(self):
        return {
            'userId': self.userId,
            'ctId': self.ctId,
            'maskId': self.maskId
        }



