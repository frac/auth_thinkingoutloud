import unittest

from .. import auth


class BaseFuncsTest(unittest.TestCase):
    """
    See if the base properties are there
    """

    def test_authenticate(self):
        """
        authenticate does the basic login, password verification
        """
        self.assertTrue(hasattr(auth, "authenticate"))

    def test_register(self):
        """
        pretty self explanatory, creates a new user
        """
        self.assertTrue(hasattr(auth, "register"))

    def test_activate(self):
        """
        Marks that the user has activate the account
        """
        self.assertTrue(hasattr(auth, "activate"))

    def test_authorize(self):
        """
        Return the user if she/he is valid
        """
        self.assertTrue(hasattr(auth, "authorize"))

