# Adopted from the works of:
# https://github.com/miguelgrinberg/api-pycon2014

import json
from base64 import b64encode

from werkzeug.exceptions import HTTPException


class TestClient:
    def __init__(self, app, auth=False, **kwargs):
        self.app = app
        if auth and 'username' in kwargs and 'password' in kwargs:
            self.auth = 'Basic ' + b64encode((kwargs['username'] + ':' +
                                              kwargs['password'])
                                             .encode('utf-8')).decode('utf-8')

    def send(self, url, method='GET', data=None, auth=False, headers={}):
        headers = headers.copy()
        if auth:
            headers['Authorization'] = self.auth
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        if data:
            data = json.dumps(data)

        with self.app.test_request_context(url, method=method, data=data,
                                           headers=headers):
            try:
                rv = self.app.preprocess_request()
                if rv is None:
                    rv = self.app.dispatch_request()
                rv = self.app.make_response(rv)
                rv = self.app.process_response(rv)
            except HTTPException as e:
                rv = self.app.handle_user_exception(e)

        return rv, json.loads(rv.data.decode('utf-8'))

    def get(self, url, auth=False, headers={}):
        return self.send(url, 'GET', headers=headers, auth=auth)

    def post(self, url, data, auth=False, headers={}):
        return self.send(url, 'POST', data, headers=headers, auth=auth)

    def put(self, url, data, auth=False, headers={}):
        return self.send(url, 'PUT', data, headers=headers, auth=auth)

    def delete(self, url, auth=False, headers={}):
        return self.send(url, 'DELETE', headers=headers, auth=auth)
