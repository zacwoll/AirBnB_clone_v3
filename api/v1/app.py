#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask, Blueprint, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS
app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close_session(response):
    """ Closes DB session """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ Handle 404 error """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host, port, threaded=True)
