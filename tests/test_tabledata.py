import unittest

from ..auth import settings
from ..auth.dbutils import DB 

import os

class DatabaseTest(unittest.TestCase):
    def setUp(self):
        settings.DATABASE_PATH = "/tmp/test.db"
        self.db = DB()
        self.assertTrue(self.db)
        self.conn = self.db.get_connection() 
        try:
            os.unlink(settings.DATABASE_PATH)
        except OSError:
            # it is ok to not exist
            pass
            
        self.assertFalse(os.path.isfile(settings.DATABASE_PATH))
        self.db.create_database()
        self.assertTrue(os.path.isfile(settings.DATABASE_PATH))


    def test_users(self):
        """
        check user database has the basic fields that we need
        """
        cur = self.conn.cursor()
        try:
            cur.execute('select id, login, salt, password from users')
        except self.conn.OperationalError:
            self.fail("user table does not contain id column")
 
    


