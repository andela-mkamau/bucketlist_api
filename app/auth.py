from flask import g
from flask_httpauth import HTTPBasicAuth

from app.errors import unauthorized
from app.models import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    """
    Callback used by HTTPAuth to check for a valid username-password
    combination.

    :param username: username of the `User`
    :param password: password of the `User`
    :return: `True` if credentials are correct; else `False`
    """
    g.user = User.query.filter_by(username=username).first()
    return g.user is not None and g.user.verify_password(password)


@auth.error_handler
def unauthorised_error():
    return unauthorized('you must authenticate to access API')
