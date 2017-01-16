from flask import request

from app import db
from app.api import api
from app.auth import auth
from app.decorators import json
from app.models import Bucketlist


@api.route('/bucketlists/<int:bucketlist_id>', methods=['GET'])
@json
@auth.login_required
def get_bucketlist(bucketlist_id):
    return Bucketlist.query.get_or_404(bucketlist_id)


@api.route('/bucketlists/', methods=['POST'])
@json
@auth.login_required
def create_bucketlist():
    bucketlist = Bucketlist().from_json(request.json)
    db.session.add(bucketlist)
    db.session.commit()
    return {}, 201, {'Location': bucketlist.get_url()}
