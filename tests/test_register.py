import unittest

from .. import auth 


class RegisterTest(unittest.TestCase):
    """
    See registering works
    """ 
    def setUp(self):
       pass 

    
    def test_register(self):
        """
        creates a new user
        """
        login = "testuser"
        password = "testpass"
        status = auth.register(login, password)
        self.assertTrue(status)

