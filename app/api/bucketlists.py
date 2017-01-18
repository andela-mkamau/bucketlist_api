from flask import request

from app import db
from app.api import api
from app.auth import auth
from app.decorators import json
from app.models import Bucketlist, Item


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


@api.route('/bucketlists/<int:bucketlist_id>', methods=['PUT'])
@json
@auth.login_required
def edit_bucketlist(bucketlist_id):
    bucketlist = Bucketlist.query.get_or_404(bucketlist_id)
    bucketlist = bucketlist.update_from_json(request.json)
    db.session.add(bucketlist)
    db.session.commit()
    return {}, 200, {'Location': bucketlist.get_url()}


@api.route('/bucketlists/<int:bucketlist_id>', methods=['DELETE'])
@json
@auth.login_required
def delete_bucketlist(bucketlist_id):
    """
    Deletes an existing Bucketlist with the given `bucketlist_id`

    :param bucketlist_id: primary key id of the Bucketlist
    :return: Response object with status code 200 if successful, else error
    """
    bucketlist = Bucketlist.query.get_or_404(bucketlist_id)
    db.session.delete(bucketlist)
    db.session.commit()
    return {}, 200


@api.route('/bucketlists/<int:bucketlist_id>/items/', methods=['POST'])
@json
@auth.login_required
def create_item(bucketlist_id):
    """
    Creates a new Item in a Bucketlist with the given `bucketlist_id`

    :param bucketlist_id: identifies the Bucketlist to create an Item in
    :return: Response with code 201 if successful, else error message
    """
    bucketlist = Bucketlist.query.get_or_404(bucketlist_id)
    item = Item().from_json(request.json)
    item.bucketlist = bucketlist
    db.session.add(item)
    db.session.commit()
    return {}, 201, {'Location': item.get_url()}


@api.route('/item/<int:item_id>')
@json
@auth.login_required
def get_item(item_id):
    return Item.query.get_or_404(item_id)
