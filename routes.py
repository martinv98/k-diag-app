from flask import jsonify
from app import db
from models import User


def init_routes(app):
    @app.route('/')
    def home():
        return jsonify({'message': 'Hello from Flask!'})

    @app.route('/add_user/<username>')
    def add_user(username):
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return f"Added {username}"

    @app.route('/get_users')
    def get_users():
        users = User.query.all()
        user_data = [{'id': user.id, 'username': user.username} for user in users]
        return jsonify(user_data)
