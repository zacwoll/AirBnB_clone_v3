#!/usr/bin/python3
""" An API for States class """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/api/v1/states', strict_slashes=False)
def all_states():
    """ GET /api/v1/states """
    states_list = [state.to_dict() for state in storage.all('State').values()]
    return jsonify(states_list)


@app_views.route('/api/v1/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """ GET /api/v1/states/<state_id> """
    try:
        state = storage.get(State, state_id).to_dict()
        return jsonify(state)
    except AttributeError:
        abort(404)


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """ DELETE /api/v1/states/<state_id> """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/api/v1/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ POST /api/v1/states """
    post_state = request.get_json()
    if not post_state:
        abort(400, {'Not a JSON'})
    elif 'name' not in post_state:
        abort(400, {'Missing name'})
    new_state = State(**post_state)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ PUT /api/v1/states/<state_id> """
    put_state = request.get_json()
    if not put_state:
        abort(400, {'Not a JSON'})
    db_state = storage.get(State, state_id)
    if not db_state:
        abort(404)
    for k, v in put_state.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(db_state, k, v)
    storage.save()
    return jsonify(db_state.to_dict())
