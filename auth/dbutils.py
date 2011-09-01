import settings
import sqlite3
from datetime import datetime

"""
This is a wrapper for a simple sqlite3 database.
I using it instead of a more complex one and a sqlalchemy middleware in order to be simple.

If by any eventuality the backend needs to be changed. Hopefully changes need to be made only to this file. 

"""



class DB(object):

    def get_connection(self):
        return sqlite3.connect(settings.DATABASE_PATH)

    def create_database(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""create table users (
                                    id INTEGER PRIMARY KEY ASC, 
                                    email text UNIQUE, 
                                    salt text, 
                                    password text,
                                    created timestamp,
                                    token text,
                                    activated timestamp 
                        )""")

        conn.commit()

    def create_user(self, email, salt, password, token):
        created = datetime.now()
        vals = (email, salt, password, created, token)
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute('INSERT into users (email, salt, password, created, token) values(?,?,?,?,?)', vals)

            conn.commit()
        
            return (True, "Success")
        except conn.IntegrityError:
            return (False, "Fail")

