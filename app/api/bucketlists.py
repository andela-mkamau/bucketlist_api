from flask import request, g

from app import db
from app.api import api
from app.auth import auth
from app.decorators import json, paginate
from app.models import Bucketlist, Item
from app.errors import not_found


@api.route('/bucketlists/<int:bucketlist_id>', methods=['GET'])
@json
@auth.login_required
def get_bucketlist(bucketlist_id):
    return Bucketlist.query.filter_by(user_id=g.user.id,
                                      id=bucketlist_id).first_or_404()


@api.route('/bucketlists/', methods=['GET'])
@paginate()
@auth.login_required
def get_all_bucketlists():
    return Bucketlist.query.filter_by(user_id=g.user.id)


@api.route('/bucketlists/', methods=['POST'])
@json
@auth.login_required
def create_bucketlist():
    bucketlist = Bucketlist().from_json(request.json)
    db.session.add(bucketlist)
    db.session.commit()
    return {
               'message': 'created bucketlist successfully',
               'resource url': bucketlist.get_url()
           }, 201, {'Location': bucketlist.get_url()}


@api.route('/bucketlists/<int:bucketlist_id>', methods=['PUT'])
@json
@auth.login_required
def edit_bucketlist(bucketlist_id):
    bucketlist = Bucketlist.query.filter_by(user_id=g.user.id,
                                            id=bucketlist_id).first_or_404()
    bucketlist = bucketlist.update_from_json(request.json)
    db.session.add(bucketlist)
    db.session.commit()
    return {
               'message': 'successfully updated bucketlist',
               'resource url': bucketlist.get_url()
           }, 200, {'Location': bucketlist.get_url()}


@api.route('/bucketlists/<int:bucketlist_id>', methods=['DELETE'])
@json
@auth.login_required
def delete_bucketlist(bucketlist_id):
    """
    Deletes an existing Bucketlist with the given `bucketlist_id`

    :param bucketlist_id: primary key id of the Bucketlist
    :return: Response object with status code 200 if successful, else error
    """
    bucketlist = Bucketlist.query.filter_by(user_id=g.user.id,
                                            id=bucketlist_id).first_or_404()
    db.session.delete(bucketlist)
    db.session.commit()
    return {}, 204


@api.route('/bucketlists/<int:bucketlist_id>/items/', methods=['POST'])
@json
@auth.login_required
def create_item(bucketlist_id):
    """
    Creates a new Item in a Bucketlist with the given `bucketlist_id`

    :param bucketlist_id: identifies the Bucketlist to create an Item in
    :return: Response with code 201 if successful, else error message
    """
    bucketlist = Bucketlist.query.filter_by(user_id=g.user.id,
                                            id=bucketlist_id).first()
    if not bucketlist:
        return not_found("cannot create item in a non-existent bucketlist")
    item = Item().from_json(request.json)
    item.bucketlist = bucketlist
    db.session.add(item)
    db.session.commit()
    return {
               "message": "successfully created item"
           }, 201, {'Location': item.get_url()}


@api.route('/item/<int:item_id>')
@json
@auth.login_required
def get_item(item_id):
    return Item.query.get_or_404(item_id)


@api.route('/bucketlists/<int:bucketlist_id>/items/<int:item_id>',
           methods=['PUT'])
@json
@auth.login_required
def edit_item(bucketlist_id, item_id):
    """
    Updates an existing Item in an existing Bucketlist

    :return: JSON Response
    """
    bucketlist = Bucketlist.query.filter_by(user_id=g.user.id,
                                            id=bucketlist_id).first()
    if not bucketlist:
        return not_found("item does not exist")
    item = Item.query.filter_by(
        id=item_id, bucketlist_id=bucketlist_id).first_or_404()
    item = item.update_from_json(request.json)
    db.session.add(item)
    db.session.commit()
    return {
               "message": "item successfully updated"
           }, 200, {'Location': item.get_url()}


@api.route('/bucketlists/<int:bucketlist_id>/items/<int:item_id>',
           methods=['DELETE'])
@json
@auth.login_required
def delete_item(bucketlist_id, item_id):
    """
    Deletes an existing Item in a Bucketlist

    :return: Response with status code 200 if successful, else JSON error
    """
    bucketlist = Bucketlist.query.filter_by(user_id=g.user.id,
                                            id=bucketlist_id).first()
    if not bucketlist:
        return not_found("item does not exist")
    item = Item.query.filter_by(id=item_id,
                                bucketlist_id=bucketlist_id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return {
               "message": "deleted item successfully"
           }, 204
