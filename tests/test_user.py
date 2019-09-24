import unittest
# Import class to be tested
from app.models import User

class UserModelTest(unittest.TestCase):
    '''
    Test class to test behaviours of the [Class] class
    Args:
        unittest.TestCase : Test case class that helps create test cases
    '''

    def setUp(self):
        self.new_user = User(password = 'banana')

    def test_password_setter(self):
        self.assertTrue(self.new_user.password_hash is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('banana'))