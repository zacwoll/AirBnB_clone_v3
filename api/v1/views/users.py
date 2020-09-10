#!/usr/bin/python3
"""
Users API module
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/api/v1/users', strict_slashes=False)
def all_users():
    """ Return JSON of all user objects """
    all_users = [user.to_dict() for user in
                 storage.all('User').values()]
    return jsonify(all_users)


@app_views.route('/api/v1/users/<user_id>', strict_slashes=False)
def get_users(user_id):
    """ Get /api/v1/users """
    try:
        user = storage.get(User, user_id).to_dict()
    except AttributeError:
        abort(404)
    return jsonify(user)


@app_views.route('/api/v1/users/<user_id>', methods=['Delete'],
                 strict_slashes=False)
def delete_user(user_id):
    """ DELETE /api/v1/users/<user_id> """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/api/v1/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ POST /api/v1/users """
    post_user = request.get_json()
    if not post_user:
        abort(400, {'Not a JSON'})
    if 'email' not in post_user:
        abort(400, {'Missing email'})
    if 'password' not in post_user:
        abort(400, {'Missing password'})
    new_user = User(**post_user)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/api/v1/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ PUT /api/v1/users/<user_id> """
    put_user = request.get_json()
    if not put_user:
        abort(400, {'Not a JSON'})
    db_user = storage.get(User, user_id)
    if not db_user:
        abort(404)
    for k, v in put_user.items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(db_user, k, v)
    storage.save()
    return jsonify(db_user.to_dict())
