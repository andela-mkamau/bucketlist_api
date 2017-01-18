from app import db
from app.models import User, Bucketlist, Item
from tests.basetest import BaseTestCase
from tests.testclient import TestClient


class BucketListAPITestCase(BaseTestCase):
    """
    Tests API functionality when using Bucketlist resource
    """
    default_username = 'user'
    default_password = 'user'

    def setUp(self):
        super().setUp()
        self.client = TestClient(self.app, auth=True,
                                 username=self.default_username,
                                 password=self.default_password)
        user = User(username=self.default_username,
                    password=self.default_password)
        bucketlist = Bucketlist(name='user bucketlist', created_by=user)
        item = Item(name='todo item', bucketlist=bucketlist)
        db.session.add_all((user, bucketlist, item))
        db.session.commit()

    def test_creates_bucketlist(self):
        """
        Should be able to create new Bucketlist
        """
        response, json = self.client.post('/api/bucketlists/',
                                          data={'name': 'test bucketlist',
                                                'user_id': 1}, auth=True)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.headers.get('Location'))

    def test_edits_bucketlist(self):
        """
        Should be able to edit an existing Bucketlist
        """
        response, json = self.client.put('/api/bucketlists/1',
                                         data={
                                             'name': 'todo list edited',
                                             'description': 'blist description'
                                         }, auth=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.headers['Location'])

    def test_deletes_bucketlist(self):
        """
        Should be able to delete an existing Bucketlist
        """
        response, json = self.client.delete('/api/bucketlists/1', auth=True)
        self.assertEqual(response.status_code, 200)

    def test_creates_new_item_in_bucketlist(self):
        """
        Should be able to create a new Item in a Bucketlist
        """
        response, json = self.client.post('/api/bucketlists/1/items/',
                                          data={
                                              'name': 'go home today',
                                              'priority': 'high'
                                          }, auth=True)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.headers.get('Location'))

    def test_updates_item_in_a_bucketlist(self):
        """
        Should be able to update an existing Item in a Bucketlist
        """
        response, json = self.client.put('/api/bucketlists/1/items/1',
                                         auth=True, data={
                                             'name': 'updated item',
                                             'done': 'true',
                                             'priority': 'very high'
                                         })
        self.assertTrue(response.status_code, 200)
        self.assertIsNotNone(response.headers.get('Location'))

    def test_deletes_item_in_bucketlist(self):
        """
        Should be able to delete an existing Item in Bucketlist
        """
        response, json = self.client.delete(
            '/api/bucketlists/1/items/1', auth=True)
        self.assertEqual(response.status_code, 200)

    def test_searches_bucketlist_by_name(self):
        """
        Should be able to do a fulltext search of Bucketlist using name
        """
        b_lists = [Bucketlist(name=n) for n in ['my blist1', 'my blist2',
                                                'your blist3',
                                                'other blists']]
        db.session.add_all(b_lists)
        db.session.commit()
        response, json = self.client.get('api/bucketlists/?q=my', auth=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['data'], [b.to_json() for b in b_lists[:2]])

