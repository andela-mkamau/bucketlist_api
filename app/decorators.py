import functools

from flask import jsonify


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
