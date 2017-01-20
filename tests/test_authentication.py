import unittest

from tests.basetest import BaseTestCase
from tests.testclient import TestClient
from app import db
from app.models import User


class UserAuthenticationTestCase(BaseTestCase):
    """
    Tests the functionality in authentication of users
    """

    def setUp(self):
        super().setUp()
        self.client = TestClient(self.app)
        user = User(username='mike',
                    password='mike')
        db.session.add(user)
        db.session.commit()

    def test_registers_user(self):
        """
        Should be able to create a new User
        """
        response, json = self.client.post('/api/auth/register', data={
            'username': 'mary', 'password': 'secret'})
        self.assertTrue(response.status_code == 201)
        self.assertTrue(json['username'] == 'mary')

    def test_logs_in_user_with_password(self):
        """
        Should be able to log in a  User
        """
        response, json = self.client.post('/api/auth/login',
                                         data={"username": "mike",
                                               "password": "mike"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['message'], 'user authenticated')

    def test_returns_error_response_for_bad_login(self):
        """
        Should return an error response for bad authentication
        """
        # No body in request
        response, json = self.client.post('/api/auth/login')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json['message'], 'no body provided in request')

        # No password in request
        response, json = self.client.post('/api/auth/login', data={
            "username": "me"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json['message'], "you must provide both username and "
                                          "password")

        # Wrong credentials
        response, json = self.client.post('/api/auth/login', data={
            "username": "me",
            "password": "my password"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json['message'], "authentication error: User does"
                                          " not exist")


if __name__ == '__main__':
    unittest.main()
