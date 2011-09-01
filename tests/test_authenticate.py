import unittest
import os

from .. import auth
from ..auth import settings
from ..auth import authenticating
from ..auth.dbutils import DB


class AuthenticateTest(unittest.TestCase):
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

    def test_authenticate(self):
        """
        authenticate does the basic login, password verification
        """

        res = auth.authenticate(self.name, self.password)
        self.assertTrue(res)

    def test_no_username(self):
        """
        email is required
        """

        try:
            auth.authenticate(None, self.password)
            self.fail("auth without email")
        except authenticating.NoEmailException:
            pass

    def test_no_password(self):
        """
        password is required
        """

        try:
            auth.authenticate(self.name, None)
            self.fail("auth without password")
        except authenticating.NoPasswordException:
            pass

    def test_wrong_username(self):
        try:
            auth.authenticate("fooz", self.password)
            self.fail("auth with wrong email")
        except authenticating.InvalidCredentialsException:
            pass

    def test_wrong_password(self):
        try:
            auth.authenticate(self.name, "fooz")
            self.fail("auth with wrong password")
        except authenticating.InvalidCredentialsException:
            pass

    def test_wrong_password_multiple_tries(self):
        """
        Accounts should be blocked after a number of wrong tries
        """
        #second user
        self.name2 = "foobar@bar.com"
        token = "token_not_activated2"
        res = self.db.create_user(self.name2, self.salt, self.hashed, token)
        self.assertTrue(res[0])
        res = self.db.activate_user(token)
        for i in range(settings.MAX_PWD_TRIES):
            try:
                auth.authenticate(self.name2, "fooz")
                self.fail("auth with wrong password")
            except authenticating.InvalidCredentialsException:
                pass
        try:
            auth.authenticate(self.name2, "fooz")
            self.fail("auth with wrong password")
        except authenticating.MaxTriesException:
            pass

    def test_a_valid_login_reset_tries(self):
        """
        when a valid login is done the tries should be reset
        """
        #second user
        self.name2 = "foobar@bar.com"
        token = "token_not_activated2"
        res = self.db.create_user(self.name2, self.salt, self.hashed, token)
        self.assertTrue(res[0])
        res = self.db.activate_user(token)

        # we do MAX_PWD_TRIES -1 tries
        for i in range(settings.MAX_PWD_TRIES - 1):
            try:
                auth.authenticate(self.name2, "fooz")
                self.fail("auth with wrong password")
            except authenticating.InvalidCredentialsException:
                pass

        #then a valid login
        res = auth.authenticate(self.name2, self.password)
        self.assertTrue(res)

        # then we do MAX_PWD_TRIES -1 tries again
        for i in range(settings.MAX_PWD_TRIES - 1):
            try:
                auth.authenticate(self.name2, "fooz")
                self.fail("auth with wrong password")
            except authenticating.InvalidCredentialsException:
                pass
