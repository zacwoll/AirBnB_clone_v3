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


@app_views.route('/api/v1/places/<place_id>/reviews', strict_slashes=False)
def all_reviews(place_id):
    """ Return JSON of all user objects """
    if not storage.get(Place, place_id):
        abort(404)
    all_reviews = [review.to_dict() for review in
                   storage.all('Review').values()
                   if place_id == review.place_id]
    return jsonify(all_reviews)


@app_views.route('/api/v1/reviews/<review_id>', strict_slashes=False)
def get_reviews(review_id):
    """ Get /api/v1/reviews """
    try:
        review = storage.get(Review, review_id).to_dict()
    except AttributeError:
        abort(404)
    return jsonify(review)


@app_views.route('/api/v1/reviews/<review_id>', methods=['Delete'],
                 strict_slashes=False)
def delete_review(review_id):
    """ DELETE /api/v1/reviews/<review_id> """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ POST /api/v1/reviews """
    post_review = request.get_json()
    if not post_review:
        abort(400, {'Not a JSON'})
    if 'text' not in post_review:
        abort(400, {'Missing text'})
    if 'user_id' not in post_review:
        abort(400, {'Missing user_id'})
    if not storage.get(User, post_review['user_id']) or \
       not storage.get(Place, place_id):
        abort(404)
    post_review['place_id'] = place_id
    new_review = Review(**post_review)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/api/v1/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ PUT /api/v1/reviews/<review_id> """
    put_review = request.get_json()
    if not put_review:
        abort(400, {'Not a JSON'})
    db_review = storage.get(Review, review_id)
    if not db_review:
        abort(404)
    for k, v in put_review.items():
        if k not in ['id', 'created_at', 'updated_at', 'user_id', 'place_id']:
            setattr(db_review, k, v)
    storage.save()
    return jsonify(db_review.to_dict()), 200
