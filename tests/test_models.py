import unittest
import time

from app.errors import ValidationError

from app import db
from app.models import User
from tests.basetest import BaseTestCase


class UserModelTestCase(BaseTestCase):
    """
    Tests the functionality of User model
    """

    def setUp(self):
        super().setUp()
        self.mike = User(username='mike', password='secret')
        db.session.add(self.mike)
        db.session.commit()

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

    def test_generate_token(self):
        token = self.mike.generate_auth_token()
        self.assertIsNotNone(token)

    def test_verifies_token(self):
        token = self.mike.generate_auth_token()
        id = User.verify_auth_token(token).id
        self.assertEqual(id, 1)

    def test_bad_token(self):
        good_token = self.mike.generate_auth_token()
        bad_token = good_token + b'bad token'
        expired_token = self.mike.generate_auth_token(1)

        with self.assertRaises(ValidationError):
            User.verify_auth_token(bad_token)

        time.sleep(1.2)
        with self.assertRaises(ValidationError):
            User.verify_auth_token(expired_token)

if __name__ == '__main__':
    unittest.main()
