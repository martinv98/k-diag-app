import json

from flask import jsonify
from app import db
from models import User
from flask import request
import bcrypt


def init_routes(app):
    @app.route('/')
    def home():
        return jsonify({'message': 'Hello from Flask!'})

    @app.route('/user/register', methods=['POST'])
    def register_user():
        data = request.json
        new_user = User(username=data['username'], email=data.get('email'),
                        password=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()))
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 200

    @app.route('/user/login', methods=['POST'])
    def login_user():
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({user}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401

    @app.route('/get_users')
    def get_users():
        users = User.query.all()
        user_data = [{'id': user.id, 'username': user.username} for user in users]
        return jsonify(user_data)
