from tests.basetest import BaseTestCase
from app.models import User

import unittest


class UserModelTestCase(BaseTestCase):
    """
    Tests the functionality of User model
    """
    def setUp(self):
        super().setUp()
        self.mike = User(username='mike', password='secret')

    def test_password_is_write_only(self):
        """
        Reading the password property should raise an AttributeError exception
        because it is a write-only property
        """
        with self.assertRaises(AttributeError):
            mike_password = self.mike.password

    def test_generate_password_hash(self):
        """
        Given a password, the User model should create a hashed password
        """
        self.assertIsNotNone(self.mike.password_hash)

    def test_verify_password(self):
        """
        A User should be able to verify their own password
        """
        self.assertTrue(self.mike.verify_password('secret'))
        self.assertFalse(self.mike.verify_password('newpassword'))


if __name__ == '__main__':
    unittest.main()

