#!/usr/bin/python3
"""
Reviews API module
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from models.amenity import Amenity


@app_views.route('/api/v1/places/<place_id>/amenities', strict_slashes=False)
def all_amenities_by_place(place_id):
    """ Return JSON of all user objects """
    db_place = storage.get(Place, place_id)
    if not db_place:
        abort(404)
    all_amenities = [amenity.to_dict() for amenity in db_place.amenities]
    return jsonify(all_amenities)


@app_views.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_place(place_id, amenity_id):
    """ DELETE /api/v1/reviews/<review_id> """
    db_place = storage.get(Place, place_id)
    db_amenity = storage.get(Amenity, amenity_id)
    if not db_place:
        abort(404)
    if not db_amenity:
        abort(404)
    try:
        db_place.amenities.remove(db_amenity)
    except ValueError:
        abort(404)
    # if db_amenity not in db_place.amenities:
    #    abort(404)
    # db_place.amenities.remove(amenity)
    storage.save()
    return {}, 200


@app_views.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """ POST /api/v1/places/<place_id>/amenities/<amenity_id> """
    db_place = storage.get(Place, place_id)
    db_amenity = storage.get(Amenity, amenity_id)
    if not db_place:
        abort(404)
    if not db_amenity:
        abort(404)
    if db_amenity in db_place.amenities:
        return jsonify(db_amenity.to_dict()), 200
    else:
        db_place.amenities.append(db_amenity)
        storage.save()
    return jsonify(db_amenity.to_dict()), 201
