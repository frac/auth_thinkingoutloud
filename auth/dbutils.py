import settings
import sqlite3
from datetime import datetime
from datetime import timedelta
from utils import create_token

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
                                    token text UNIQUE,
                                    activated timestamp,
                                    tries INTEGER default 0, 
                                    auth_token text UNIQUE
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

    def get_user_by_token(self, token):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT created, token, activated from users where token = ? ', (token,))
    
        return cur.fetchall()

    def activate_user(self, token):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('update users set activated = ? where token = ? and activated is NULL ', (datetime.now(),token,))
        conn.commit() 

    def get_user_by_email(self, email):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT salt, password, activated, tries from users where email = ? ', (email,))
    
        return cur.fetchall()

    def failed_login(self, email):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('update users set tries = tries + 1 where email = ? ', (email,))
        conn.commit() 

    def successful_login(self, email):
        conn = self.get_connection()
        auth_token = create_token()
        cur = conn.cursor()
        cur.execute('update users set tries = 0, auth_token=? where email = ? ', (auth_token,email,))
        conn.commit() 
        return auth_token
    
    def get_user_by_auth_token(self, auth_token):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT email from users where auth_token = ? ', (auth_token,))
    
        return cur.fetchall()

    def decrease_pwd_tries(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('update users set tries = tries - 1 where tries > 0 ')
        conn.commit() 

    def remove_inactive_users(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('delete from users where activated is NULL and created <= ? ', 
                            (datetime.now() - timedelta(days=settings.DAYS_TO_ACTIVATE), ))
        conn.commit() 

