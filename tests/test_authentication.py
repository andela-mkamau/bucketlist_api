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


if __name__ == '__main__':
    unittest.main()
