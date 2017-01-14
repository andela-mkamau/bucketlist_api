from tests.basetest import BaseTestCase
from app.models import User

import unittest


class UserModelTestCase(BaseTestCase):
    """
    Tests the functionality of User model
    """

    def test_reading_password_property_raises_exception(self):
        """
        Reading the password property should raise an AttributeError exception
        because it is a write-only property
        """
        mike = User(username='mike', password='secret')
        with self.assertRaises(AttributeError):
            mike_password = mike.password

    def test_generates_password_hash(self):
        """
        Given a password, the User model should create a hashed password
        """
        alla = User(password='my password')
        self.assertIsNotNone(alla.password_hash)


if __name__ == '__main__':
    unittest.main()

