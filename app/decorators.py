# Inspired by the works of:
# https://github.com/miguelgrinberg/api-pycon2014

import functools

from flask import jsonify, Response
from flask import request, url_for

from app.errors import unauthorized, bad_request
from app.models import Bucketlist


def paginate(max_per_page=20):
    """
    Decorator to paginate the result of a query
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            # Default items per page is 20, max is 100
            #per_page = min(request.args.get('limit', 20, type=int), 100)
            page = request.args.get('page', 1, type=int)
            query = func(*args, **kwargs)
            if not request.args:
                bucketlists = query.all()
                if bucketlists:
                    return jsonify([blist.to_json() for blist in bucketlists])
                else:
                    return jsonify({"message": "user has no bucketlists"})
            if not all([key in ('q', 'limit', 'page') for key in request.args.keys()]):
                return bad_request('unknown arguments in request')
            per_page = min(request.args.get('limit', 20, type=int), 100)
            if 'q' in request.args:
                query = query.filter(Bucketlist.name.like('%' +
                                                          request.args['q']
                                                          + '%'))
            result_pages = query.paginate(page, per_page)
            pages_meta = {
                'page': page, 'per_page': per_page,
                'total': result_pages.total,
                'pages': result_pages.pages
            }
            if result_pages.has_prev:
                pages_meta['prev'] = url_for(request.endpoint,
                                             page=result_pages.prev_num,
                                             limit=per_page,
                                             _external=True, **kwargs)
            else:
                pages_meta['prev'] = None

            if result_pages.has_next:
                pages_meta['next'] = url_for(request.endpoint,
                                             page=result_pages.next_num,
                                             limit=per_page,
                                             _external=True, **kwargs)
            else:
                pages_meta['next'] = None

            pages_meta['first'] = url_for(request.endpoint,
                                          page=1,
                                          limit=per_page,
                                          _external=True, **kwargs)
            pages_meta['last'] = url_for(request.endpoint,
                                         page=result_pages.pages,
                                         limit=per_page,
                                         _external=True, **kwargs)
            return jsonify({
                'data': [item.to_json() for item in result_pages.items],
                'urls': [item.get_url() for item in result_pages.items],
                'meta': pages_meta
            })

        return wrapped

    return decorator


def json(func):
    """
    Decorator to convert response objects to JSON format.

    NOTE: The response is taken to have the general format :
            `(response_data, [status_code, [headers]])`
         where `status_code` and `headers` are optional

    :param func: function to decorate
    :return: decorated function, whose return value is a jsonified response
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        response = func(*args, **kwargs)
        status_or_headers = None
        headers = None
        if isinstance(response, tuple):
            response, status_or_headers, headers = response + (None,) * (
                3 - len(response))
        if isinstance(status_or_headers, (dict, list)):
            # these are headers, NOT status codes
            headers, status_or_headers = status_or_headers, None
        if isinstance(response, Response):
            return response
        if not isinstance(response, dict):
            response = response.to_json()
        response = jsonify(response)
        if status_or_headers is not None:
            # this is a status code
            response.status_code = status_or_headers
        if headers is not None:
            response.headers.extend(headers)
        return response

    return wrapped
