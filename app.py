from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    with app.app_context():
        from models import User
        from models import CTScan
        from models import Mask
        from models import Instance
        db.create_all()

    from routes import init_routes
    init_routes(app)

    return app
