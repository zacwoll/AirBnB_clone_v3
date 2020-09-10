#!/usr/bin/python3
"""
Places API module
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/api/v1/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """ Return JSON of all user objects """
    if not storage.get(City, city_id):
        abort(404)
    all_places = [place.to_dict() for place in
                  storage.all('Place').values() if city_id == place.city_id]
    return jsonify(all_places)


@app_views.route('/api/v1/places/<place_id>', strict_slashes=False)
def get_places(place_id):
    """ Get /api/v1/places """
    try:
        place = storage.get(Place, place_id).to_dict()
    except AttributeError:
        abort(404)
    return jsonify(place)


@app_views.route('/api/v1/places/<place_id>', methods=['Delete'],
                 strict_slashes=False)
def delete_place(place_id):
    """ DELETE /api/v1/places/<place_id> """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/api/v1/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ POST /api/v1/places """
    post_place = request.get_json()
    if not post_place:
        abort(400, {'Not a JSON'})
    if 'name' not in post_place:
        abort(400, {'Missing name'})
    if 'user_id' not in post_place:
        abort(400, {'Missing user_id'})
    if not storage.get(User, post_place['user_id']) or \
       not storage.get(City, city_id):
        abort(404)
    post_place['city_id'] = city_id
    new_place = Place(**post_place)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/api/v1/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ PUT /api/v1/places/<place_id> """
    put_place = request.get_json()
    if not put_place:
        abort(400, {'Not a JSON'})
    db_place = storage.get(Place, place_id)
    if not db_place:
        abort(404)
    for k, v in put_place.items():
        if k not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(db_place, k, v)
    storage.save()
    return jsonify(db_place.to_dict())
