#!/usr/bin/python3
"""
Cities class for api
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import City
from models import State


@app_views.route('/api/v1/states/<state_id>/cities', strict_slashes=False)
def all_cities(state_id):
    """ GET /api/v1/states/<state_id>/cities"""
    if not storage.get(State, state_id):
        abort(404)
    city_list = [city.to_dict() for city in
                 storage.all("City").values() if state_id == city.state_id]
    return jsonify(city_list)


@app_views.route('/api/v1/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """ GET /api/v1/cities/<city_id> """
    try:
        city = storage.get(City, city_id).to_dict()
        return jsonify(city)
    except:
        abort(404)


@app_views.route('/api/v1/cities/<city_id>',
                 strict_slashes=False, methods=["DELETE"])
def delete_city(city_id):
    """ DELETE /api/v1/cities/<city_id> """
    try:
        city = storage.get(City, city_id)
        storage.delete(city)
        storage.save()
        return {}, 200
    except:
        abort(404)


@app_views.route('/api/v1/states/<state_id>/cities/',
                 strict_slashes=False, methods=["POST"])
def create_city(state_id):
    """ POST /api/v1/states/<state_id>/cities """
    city_name = request.get_json()
    if not storage.get(State, state_id):
        abort(404)
    if not city_name:
        abort(400, {"Not a JSON"})
    elif 'name' not in city_name:
        abort(400, {"Missing name"})
    new_city = City(**city_name)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/api/v1/cities/<city_id>/',
                 strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """PUT /api/v1/cities/<city_id> """
    get_city = request.get_json()
    if not get_city:
        abort(400, "{Not a JSON}")
    try:
        city = storage.get(City, city_id)
    except KeyError:
        abort(404)
    for k, v in get_city.items():
        setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict())
