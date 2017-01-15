# Adopted from the works of:
# https://github.com/miguelgrinberg/api-pycon2014

from flask import jsonify


class ValidationError(ValueError):
    pass


def bad_request(message):
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': message})
    response.status_code = 401
    return response
