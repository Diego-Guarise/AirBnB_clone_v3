#!/usr/bin/python3
"""All User CRUD operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
def get_users():
    """get all User objects"""
    if request.method == 'GET':
        users = storage.all(User).values()
        users_dict = []
        for user in users:
            users_dict.append(user.to_dict())
        return jsonify(users_dict)
    else:
        """creates a new User object"""
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return (jsonify("Not a JSON"), 400)
        user_dict = request.get_json()
        if "email" not in user_dict:
            return jsonify("Missing email"), 400
        if "password" not in user_dict:
            return jsonify("Missing password"), 400
        new_user = User(**user_dict)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_user(user_id):
    """get User object by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        """display User"""
        return jsonify(user.to_dict())
    elif request.method == 'PUT':
        """updates User"""
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return (jsonify("Not a JSON"), 400)
        user_dict = request.get_json()
        if "password" in user_dict:
            user.password = user_dict["password"]
        if "first_name" in user_dict:
            user.first_name = user_dict["first_name"]
        if "last_name" in user_dict:
            user.last_name = user_dict["last_name"]
        storage.save()
        return jsonify(user.to_dict()), 200
    else:
        """deletes a User"""
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
