#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(response):
    """ Closes DB session """
    storage.close()

@app.route('/', strict_slashes=False)
def index():
    """returns Hello HBNB!"""
    return 'Hello HBNB!'


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host, port, threaded=True)
