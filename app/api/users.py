# Users -- as an API resource
from flask import request

from app import db
from app.api import api
from app.decorators import json
from app.models import User


@api.route('/auth/register', methods=['POST'])
@json
def register_user():
    """
    Registers a new User with data from the POST request
    """
    user = User().from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return user, 201

@api.route('/auth/login', methods=['POST'])
@json
def login_user():
    """
    Logs in a User using a token or username-password combination. The user is
    given an authentication token valid for 60 minutes

    :return: JSON Response object with status code 200 on success, else error
    """
    user = User().from_login_json(request.json)
    token = user.generate_auth_token()
    return {'token': token.decode('ascii'),
            'message':'user authenticated'}, 200
