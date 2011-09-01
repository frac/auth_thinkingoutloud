import unittest
import os

from .. import auth
from ..auth import settings
from ..auth import cleanup
from ..auth.dbutils import DB


class CleanupTest(unittest.TestCase):
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
        try:
            self.auth_token = auth.authenticate(self.name, "foo")
        except auth.AuthException:
            pass

        self.name1 = "foo1@bar.com"
        res = self.db.create_user(self.name1, self.salt, self.hashed, token)
            

    def test_clean_tries(self):
        """
        remove failed tries from the db 
        """
        conn = self.db.get_connection()
        cur = conn.cursor()
        
        cur.execute('SELECT tries from users where email = ? ', (self.name,))
        tries = cur.fetchall()[0][0]

        self.assertEqual(tries,1)

        cleanup.cleanup()

        cur.execute('SELECT tries from users where email = ? ', (self.name,))
        tries = cur.fetchall()[0][0]

        self.assertEqual(tries,0)

