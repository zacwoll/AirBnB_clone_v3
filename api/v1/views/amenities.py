#!/usr/bin/python3
"""
Amenities API module
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/api/v1/amenities', strict_slashes=False)
def all_amenities():
    """ Return JSON of all amenity objects """
    all_amenities = [amenity.to_dict() for amenity in
                     storage.all('Amenity').values()]
    return jsonify(all_amenities)


@app_views.route('/api/v1/amenities/<amenity_id>', strict_slashes=False)
def get_amenities(amenity_id):
    """ Get /api/v1/amenities """
    try:
        amenity = storage.get(Amenity, amenity_id).to_dict()
    except AttributeError:
        abort(404)
    return jsonify(amenity)


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['Delete'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ DELETE /api/v1/amenities/<amenity_id> """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/api/v1/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ POST /api/v1/amenities """
    post_amenity = request.get_json()
    if not post_amenity:
        abort(400, {'Not a JSON'})
    if 'name' not in post_amenity:
        abort(400, {'Missing name'})
    new_amenity = Amenity(**post_amenity)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ PUT /api/v1/amenities/<amenity_id> """
    put_amenity = request.get_json()
    if not put_amenity:
        abort(400, {'Not a JSON'})
    db_amenity = storage.get(Amenity, amenity_id)
    if not db_amenity:
        abort(404)
    for k, v in put_amenity.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(db_amenity, k, v)
    storage.save()
    return jsonify(db_amenity.to_dict()), 200
