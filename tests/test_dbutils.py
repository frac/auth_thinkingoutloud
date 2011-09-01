import unittest

from ..auth import settings
from ..auth.dbutils import DB 

import os

class DatabaseTest(unittest.TestCase):
    def setUp(self):
        settings.DATABASE_PATH = "/tmp/test.db"
        self.db = DB()
        self.assertTrue(self.db)

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
        conn = self.db.get_connection()
        cur = conn.cursor()
        try:
            cur.execute('select * from users')
        except self.conn.OperationalError:
            self.fail("user table not created")
 
    
    def test_create_user(self):
        """
        test low level user creation
        """
        name = "foo"
        salt = "bar"
        password = "foozbarz"
        token = "cheese"

        try:
            os.unlink(settings.DATABASE_PATH)
        except OSError:
            # it is ok to not exist
            pass
            
        self.db.create_database()
        res = self.db.create_user(name, salt, password, token)
        self.assertTrue(res)
        conn = self.db.get_connection()
        try:
            cur = conn.cursor()
            cur.execute('select email, salt, password, created, token, activated from users')
            users = cur.fetchall()
            self.assertEqual(len(users),1)
            user = users[0]
            self.assertEqual(name,user[0])
            self.assertEqual(salt,user[1])
            self.assertEqual(password,user[2])
            self.assertFalse(user[3] is None)
            self.assertEqual(token,user[4])
            self.assertTrue(user[5] is None)

        except conn.OperationalError, e:
            self.fail("Test user creation %s" % e)

