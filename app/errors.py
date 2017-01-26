# Adopted from the works of:
# https://github.com/miguelgrinberg/api-pycon2014

from flask import jsonify

class UnauthorizedError(Exception):
    pass

class ConflictError(ValueError):
    pass

class ValidationError(ValueError):
    pass


def not_found(message):
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': message})
    response.status_code = 404
    return response


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

def conflict(message):
    response = jsonify({'status': 409, 'error': 'resource already exists',
                        'message': message})
    response.status_code = 409
    return response