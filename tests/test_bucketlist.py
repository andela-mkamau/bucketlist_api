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
