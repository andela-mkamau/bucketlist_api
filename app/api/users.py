# Users -- as an API resource
from flask import request, jsonify, abort

from app.api import api
from app import db
from app.models import User
from app.decorators import json


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
