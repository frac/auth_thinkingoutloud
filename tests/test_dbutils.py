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

    def test_get_connection(self):
        """
        In the prototype I'm using sqllite that will not deal with concurrent accesses
         
        """
        conn2 = self.db.get_connection() 
        self.assertTrue(conn2)


    def test_create(self):
        """
        check database creation
        """
        try:
            os.unlink(settings.DATABASE_PATH)
        except OSError:
            # it is ok to not exist
            pass
            
        self.assertFalse(os.path.isfile(settings.DATABASE_PATH))
        self.db.create_database()
        self.assertTrue(os.path.isfile(settings.DATABASE_PATH))
        cur = self.conn.cursor()
        try:
            cur.execute('select * from users')
        except self.conn.OperationalError:
            self.fail("user table not created")
 
    


