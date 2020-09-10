#!/usr/bin/python3
"""
Cities class for api
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


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
    except AttributeError:
        abort(404)


@app_views.route('/api/v1/cities/<city_id>',
                 strict_slashes=False, methods=["DELETE"])
def delete_city(city_id):
    """ DELETE /api/v1/cities/<city_id> """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/api/v1/states/<state_id>/cities/',
                 strict_slashes=False, methods=["POST"])
def create_city(state_id):
    """ POST /api/v1/states/<state_id>/cities """
    post_city = request.get_json()
    if not storage.get(State, state_id):
        abort(404)
    if not post_city:
        abort(400, {"Not a JSON"})
    elif 'name' not in post_city:
        abort(400, {"Missing name"})
    post_city['state_id'] = state_id
    new_city = City(**post_city)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/api/v1/cities/<city_id>/',
                 strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """ PUT /api/v1/cities/<city_id> """
    put_city = request.get_json()
    if not put_city:
        abort(400, "{Not a JSON}")
    db_city = storage.get(City, city_id)
    if not db_city:
        abort(404)
    for k, v in put_city.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(db_city, k, v)
    storage.save()
    return jsonify(db_city.to_dict()), 200
