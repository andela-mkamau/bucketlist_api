from flask import Blueprint, g

from app.errors import (bad_request, ValidationError, not_found, ConflictError,
                        conflict)

# API Blueprint
api = Blueprint('api', __name__)


@api.errorhandler(ConflictError)
def conflict_error(e):
    return conflict(e.args[0])


@api.errorhandler(404)
def not_found_error(e):
    return not_found('item not found')


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])


@api.errorhandler(400)
def bad_request_error(e):
    return bad_request("invalid request")


@api.after_request
def after_request(response):
    if hasattr(g, 'headers'):
        response.headers.extend(g.headers)
    return response


from app.api import users, bucketlists
