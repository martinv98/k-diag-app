import json

from flask import jsonify
from app import db
from models import User, CTScan, Mask, Instance
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
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 400
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=data['username'], email=data.get('email'), password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'username': data['username']}), 200

    @app.route('/user/login', methods=['POST'])
    def login_user():
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
            print("Login successful. Username in DB: " + user.username + " Hashed password in DB: " + user.password.decode('utf-8'))
            print("Username from FE: " + data['username'] + " Password from FE: " + data['password'])
            return jsonify({'username': data['username']}), 200
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

        return jsonify({'message': 'File uploaded successfully'}), 200

    @app.route('/finish_upload', methods=['POST'])
    def finish_upload():
        data = request.json
        print(data)

        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        file_dcom: CTScan = CTScan(filename=data['dcom'], metadataCT='dcom', userId=user.id)
        db.session.add(file_dcom)
        db.session.commit()
        file_mask: Mask = Mask(filename=data['mask'], metadataMask='mask', userId=user.id)
        db.session.add(file_mask)
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully'}), 200
