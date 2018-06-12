"""
custom response for bad requests
"""
from flask.json import jsonify


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response
