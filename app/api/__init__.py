from flask import Blueprint

from app.errors import bad_request, ValidationError, not_found

# API Blueprint
api = Blueprint('api', __name__)


@api.errorhandler(404)
def not_found_error(e):
    return not_found('item not found')


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])


@api.errorhandler(400)
def bad_request_error(e):
    return bad_request('invalid request')


from app.api import users, bucketlists
