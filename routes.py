import json

from flask import jsonify
from app import db
from models import User
from flask import request
import bcrypt
import os


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

    UPLOAD_FOLDER = 'dicoms/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route('/upload_scan', methods=['POST'])
    def upload_scan():
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400

        # Here you can save the file or process it as needed
        # For example, save it to a specific directory:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        return 'File uploaded successfully', 200