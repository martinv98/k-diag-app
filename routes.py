import json

from flask import jsonify
from app import db
from models import User, CTScan, Mask, Instance
from flask import request
import bcrypt
import os
import random


def init_routes(app):
    @app.route('/')
    def home():
        return jsonify({'message': 'Hello from Flask!'}), 200, {'Access-Control-Allow-Origin': '*'}

    @app.route('/user/register', methods=['POST'])
    def register_user():
        data = request.json
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 400, {'Access-Control-Allow-Origin': '*'}
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=data['username'], email=data.get('email'), password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'username': data['username']}), 200, {'Access-Control-Allow-Origin': '*'}

    @app.route('/user/login', methods=['POST'])
    def login_user():
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
            print(
                "Login successful. Username in DB: " + user.username + " Hashed password in DB: " + user.password.decode(
                    'utf-8'))
            print("Username from FE: " + data['username'] + " Password from FE: " + data['password'])
            return jsonify({'username': data['username']}), 200, {'Access-Control-Allow-Origin': '*'}
        else:
            return jsonify({'message': 'Invalid username or password'}), 401, {'Access-Control-Allow-Origin': '*'}

    @app.route('/get_users')
    def get_users():
        users = User.query.all()
        user_data = [{'id': user.id, 'username': user.username} for user in users]
        return jsonify(user_data), 200, {'Access-Control-Allow-Origin': '*'}

    UPLOAD_FOLDER = '/app/instance/dicoms'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route('/upload_scan', methods=['POST'])
    def upload_scan():
        if 'file' not in request.files:
            return 'No file part', 400, {'Access-Control-Allow-Origin': '*'}

        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400, {'Access-Control-Allow-Origin': '*'}

        # Here you can save the file or process it as needed
        # For example, save it to a specific directory:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        return jsonify({'message': 'File uploaded successfully'}), 200, {'Access-Control-Allow-Origin': '*'}

    @app.route('/finish_upload', methods=['POST'])
    def finish_upload():
        data = request.json
        print(data)

        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404, {'Access-Control-Allow-Origin': '*'}

        file_dcom: CTScan = CTScan(filename=data['dcom'], metadataCT='dcom')
        db.session.add(file_dcom)
        db.session.commit()
        file_mask: Mask = Mask(filename=data['mask'], metadataMask='mask')
        db.session.add(file_mask)
        db.session.commit()

        result = bool(random.getrandbits(1))
        accuracy = random.uniform(30, 70)
        instance = Instance(userId=user.userId, ctId=file_dcom.ctId, maskId=file_mask.maskId, result=result,
                            resultAccuracy=accuracy)
        db.session.add(instance)
        db.session.commit()
        return jsonify({'message': 'File uploaded successfully', 'result': result, 'accuracy': accuracy}), 200, {'Access-Control-Allow-Origin': '*'}

    @app.route('/get_instances/<username>', methods=['GET'])
    def get_instances(username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404, {'Access-Control-Allow-Origin': '*'}
        instances = Instance.query.filter_by(userId=user.userId).all()
        instance_data = [{'ctId': instance.ctId, 'maskId': instance.maskId, 'accuracy': instance.resultAccuracy,
                          'result': instance.result} for instance in instances]
        return jsonify(instance_data), 200, {'Access-Control-Allow-Origin': '*'}
