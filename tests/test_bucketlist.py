import json

import datetime

from app import db
from app.models import User, Bucketlist, Item
from tests.basetest import BaseTestCase


class BucketListAPITestCase(BaseTestCase):
    """
    Tests API functionality when using Bucketlist resource
    """
    default_username = 'user'
    default_password = 'user'

    def setUp(self):
        super().setUp()
        user = User(username=self.default_username,
                    password=self.default_password)
        db.session.add(user)
        db.session.commit()

        token = user.generate_auth_token()
        self.valid_token = 'Bearer {}'.format(token.decode('ascii'))

        bucketlist = Bucketlist(name='user bucketlist', created_by=user)
        item = Item(name='todo item', bucketlist=bucketlist)

        self.client = self.app.test_client()

        db.session.add_all((bucketlist, item))
        db.session.commit()

    def test_get_bucketlist(self):
        response = self.client.get('/api/bucketlists/1',
                                   headers=self.get_headers(self.valid_token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, json.loads(response.get_data(as_text=True))['id'])

    def test_create_bucketlist(self):
        """
        Should be able to create new Bucketlist
        """
        response = self.client.post('/api/bucketlists/',
                                    headers=self.get_headers(self.valid_token),
                                    data=json.dumps({
                                        'name': 'test bucketlist'
                                    }))
        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(response.headers.get('Location'))

    def test_create_bucketlist_with_invalid_data(self):
        """
        For a POST request with invalid data, creating a Bucketlist returns
        an error Response

        """
        # No data provided
        response = self.client.post('/api/bucketlists/', data=json.dumps({}),
                                    headers=self.get_headers(self.valid_token))
        self.assertEqual(response.status_code, 400)
        self.assertEqual("invalid request: no data provided", json.loads(
            response.get_data(as_text=True))['message'])

        # empty name
        response = self.client.post('/api/bucketlists/',
                                    headers=self.get_headers(self.valid_token),
                                    data=json.dumps({'name': ''}))
        self.assertEqual(response.status_code, 400)
        self.assertEqual('bucketlist name cannot be empty', json.loads(
            response.get_data(as_text=True))['message'])

    def test_edit_bucketlist(self):
        """
        Should be able to edit an existing Bucketlist
        """
        response = self.client.put('/api/bucketlists/1',
                                   data=json.dumps({
                                       'name': 'todo list edited',
                                       'description': 'blist description'
                                   }),
                                   headers=self.get_headers(self.valid_token))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.headers.get('Location'))

    def test_delete_bucketlist(self):
        """
        Should be able to delete an existing Bucketlist
        """
        response = self.client.delete('/api/bucketlists/1', headers=
        self.get_headers(self.valid_token))
        self.assertEqual(response.status_code, 200)

    def test_delete_non_existent_bucketlist(self):
        """
        Should return an error response when deleting a non-existent bucketlist
        """
        response = self.client.delete('/api/bucketlists/1233', headers=
        self.get_headers(self.valid_token))
        self.assertEqual(response.status_code, 404)

    def test_create_new_item_in_bucketlist(self):
        """
        Should be able to create a new Item in a Bucketlist
        """
        response = self.client.post('/api/bucketlists/1/items/',
                                    data=json.dumps({
                                        'name': 'go home today',
                                        'priority': 'high'
                                    }),
                                    headers=self.get_headers(self.valid_token))
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.headers.get('Location'))

    def test_create_item_with_invalid_data(self):
        """
        Should return an error response when creating an Item with invalid
        data
        """
        # Empty data
        response = self.client.post('/api/bucketlists/1/items/',
                                    data=json.dumps({}),
                                    headers=self.get_headers(
                                        self.valid_token))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.get_data(as_text=True))['message'],
            'invalid request: no JSON data has been provided to construct Item')

    def test_update_item_in_a_bucketlist(self):
        """
        Should be able to update an existing Item in a Bucketlist
        """
        response = self.client.put('/api/bucketlists/1/items/1',
                                   data=json.dumps({
                                       'name': 'updated item',
                                       'done': 'true',
                                       'priority': 'very high'
                                   }),
                                   headers=self.get_headers(self.valid_token))
        self.assertTrue(response.status_code, 200)
        self.assertIsNotNone(response.headers.get('Location'))

    def test_delete_item_in_bucketlist(self):
        """
        Should be able to delete an existing Item in Bucketlist
        """
        response = self.client.delete('/api/bucketlists/1/items/1',
                                      headers=self.get_headers(
                                          self.valid_token))
        self.assertEqual(response.status_code, 200)

    def test_search_bucketlist_by_name(self):
        """
        Should be able to do a fulltext search of Bucketlist using name
        """
        b_lists = [Bucketlist(name=n) for n in ['my blist1', 'my blist2',
                                                'your blist3',
                                                'other blists']]
        db.session.add_all(b_lists)
        db.session.commit()
        response = self.client.get('api/bucketlists/?q=my',
                                   headers=self.get_headers(
                                       self.valid_token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True))['data'],
                         [b.to_json() for b in b_lists[:2]])
