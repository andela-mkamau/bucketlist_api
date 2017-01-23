import json
import unittest

from app import db
from app.models import User
from tests.basetest import BaseTestCase


class UserAuthenticationTestCase(BaseTestCase):
    """
    Tests the functionality in authentication of users
    """

    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()
        user = User(username='mike',
                    password='mike')
        db.session.add(user)
        db.session.commit()

    def test_register_user(self):
        """
        Should be able to create a new User
        """
        response = self.client.post('/api/auth/register',
                                    data=json.dumps({
                                        'username': 'mary',
                                        'password': 'secret'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            json.loads(response.get_data(as_text=True))['username'], 'mary')

    def test_register_duplicate_user(self):
        """
        Should return an error response for duplicate registration of users
        """
        response = self.client.post('/api/auth/register',
                                    data=json.dumps({
                                        'username': 'mike',
                                        'password': 'secret'}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            json.loads(response.get_data(as_text=True))['message'],
            'user already exists')

    def test_log_in_user_with_password(self):
        """
        Should be able to log in a  User using username-password credentials
        """
        response = self.client.post('/api/auth/login',
                                    data=json.dumps({"username": "mike",
                                                     "password": "mike"}),
                                    headers=self.get_headers()
                                    )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.get_data(as_text=True))['message'],
            'user authenticated')

    def test_bad_login(self):
        """
        Should return an error response for bad authentication
        """
        # No body in request
        response = self.client.post('/api/auth/login', data=json.dumps({}),
                                    headers=self.get_headers())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.get_data(as_text=True))['message'],
            'no body provided in request')

        # No password in request
        response = self.client.post('/api/auth/login', data=json.dumps({
            "username": "me"
        }), headers=self.get_headers())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.get_data(as_text=True))['message'],
            "you must provide both username and password")

        # Wrong credentials
        response = self.client.post('/api/auth/login', data=json.dumps({
            "username": "me",
            "password": "my password"
        }), headers=self.get_headers())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.get_data(as_text=True))['message'],
            "authentication error: User does not exist")


if __name__ == '__main__':
    unittest.main()
