from flask import g
from flask_httpauth import HTTPTokenAuth

from app.errors import unauthorized
from app.models import User

auth = HTTPTokenAuth('Bearer')


@auth.verify_token
def verify_token(token):
    """
    Callback used by HTTPAuth to check for a valid token

    :param token: token provided to the `User`
    :return: `True` if credentials are correct; else `False`
    """
    g.user = User.verify_auth_token(token)
    return g.user is not None


@auth.error_handler
def unauthorised_error():
    return unauthorized('you must authenticate to access API')
