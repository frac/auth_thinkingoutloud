import unittest
import os
import datetime

import fudge

from .. import auth
from ..auth import settings
from ..auth import activating
from ..auth.dbutils import DB


class ActivateTest(unittest.TestCase):
    """
    See if user activation works
    """

    def setUp(self):
        """
        rather large setup that adds users to the database
        """
        settings.DATABASE_PATH = "/tmp/test.db"
        self.db = DB()
        self.assertTrue(self.db)
        name = "foo"
        salt = "bar"
        password = "foozbarz"
        self.token = "token_not_activated"

        try:
            os.unlink(settings.DATABASE_PATH)
        except OSError:
            # it is ok to not exist
            pass

        self.db.create_database()
        res = self.db.create_user(name, salt, password, self.token)
        self.assertTrue(res[0])
        now = datetime.datetime.now()
        self.future = datetime.datetime(now.year + 1, now.month, now.day)

    def test_activate(self):
        """
        activate the user
        """
        res = auth.activate(self.token)
        self.assertTrue(res)

        # multiple activations are not allowed
        try:
            auth.activate(self.token)
            self.fail("should not activate multiple times")
        except activating.UserAlreadyActivatedException:
            pass

    @fudge.patch('datetime.datetime')
    def test_late_activation(self, FakeNow):
        (FakeNow.expects('now')
                 .returns(self.future))

        try:
            auth.activate(self.token)
            self.fail("Token expired")
        except activating.UserExpiredException:
            pass

    def test_user_not_found(self):
        """
        activate the user
        """
        try:
            auth.activate("")
            self.fail("user should not be found")
        except activating.UserNotFoundException:
            pass
