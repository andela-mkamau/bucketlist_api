import unittest

from tests.basetest import BaseTestCase
from tests.testclient import TestClient


class UserAuthenticationTestCase(BaseTestCase):
    """
    Tests the functionality in authentication of users
    """

    def setUp(self):
        super().setUp()
        self.client = TestClient(self.app)

    def test_registers_user(self):
        """
        Should be able to create a new User
        """
        response, json = self.client.post('/api/auth/register', data={
            'username': 'mary', 'password': 'secret'})
        self.assertTrue(response.status_code == 201)
        self.assertTrue(json['username'] == 'mary')


if __name__ == '__main__':
    unittest.main()
