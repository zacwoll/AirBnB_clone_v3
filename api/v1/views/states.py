#!/usr/bin/python3
""" An API for States class """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/api/v1/states', strict_slashes=False)
def all_states():
    """ GET /api/v1/states """
    all_states = [state.to_dict() for state in storage.all('State').values()]
    return jsonify(all_states)


@app_views.route('/api/v1/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """ GET /api/v1/states/<state_id> """
    try:
        state = storage.get(State, state_id).to_dict()
        return jsonify(state)
    except:
        abort(404)

@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """ DELETE /api/v1/states/<state_id> """
    try:
        state = storage.get(State, state_id)
        state.delete()
        storage.delete(state)
        storage.save()
        return {}, 200
    except:
        abort(404)


@app_views.route('/api/v1/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ POST /api/v1/states """
    state_name = request.get_json()
    if not state_name:
        abort(400, {'Not a JSON'})
    elif 'name' not in state_name:
        abort(400, {'Missing name'})
    new_state = State(**state_name)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ PUT /api/v1/states/<state_id> """
    get_state = request.get_json()
    if not get_state:
        abort(400, {'Not a JSON'})
    try:
        state = storage.get(State, state_id)
    except KeyError:
        abort(404)
    for k, v in get_state.items():
        setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict())
