#!/usr/bin/python3
"""
Create a route to check on status
"""
from flask import Flask
from api.v1.views import app_views
from models import storage


@app_views.route('/api/v1/status', strict_slashes=False)
def status():
    """ Return 'OK' """
    return {"status": "OK"}


@app_views.route('/api/v1/stats', strict_slashes=False)
def stats():
    """ Retrieve stats from DB """
    return {"amenities": storage.count('Amenity'),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")}
