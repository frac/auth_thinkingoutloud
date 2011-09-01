import unittest
import os

from .. import auth
from ..auth import settings
from ..auth.dbutils import DB


class AuthorizeTest(unittest.TestCase):
    """
    authentication rules
    """
    def setUp(self):
        """
        rather large setup that adds users to the database
        """
        settings.DATABASE_PATH = "/tmp/test.db"
        self.db = DB()
        self.assertTrue(self.db)
        self.name = "foo@bar.com"
        self.salt = "bar"
        self.password = "foozbarz"
        self.hashed = "17e579033050131929d85f4b999cf24b76274890"
        token = "token_not_activated"

        try:
            os.unlink(settings.DATABASE_PATH)
        except OSError:
            # it is ok to not exist
            pass

        self.db.create_database()
        res = self.db.create_user(self.name, self.salt, self.hashed, token)
        self.assertTrue(res[0])
        res = self.db.activate_user(token)
        self.auth_token = auth.authenticate(self.name, self.password)

    def test_authorization(self):
        """
        Checks to see if the auth_token is valid.
        """

        self.assertTrue(auth.authorize(self.auth_token))

    def test_wrong_creds(self):
        """
        Invalid credencials should not be accepted
        """

        self.assertFalse(auth.authorize("bar"))

    def test_empty_creds(self):
        """
        Empty credencials should not be accepted
        """
        self.assertFalse(auth.authorize(None))
