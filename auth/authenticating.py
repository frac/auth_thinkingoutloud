from hashlib import sha1

from dbutils import DB
import settings

class AuthException(Exception):
    pass

class NoEmailException(AuthException):
    pass

class NoPasswordException(AuthException):
    pass

class InvalidCredentialsException(AuthException):
    pass

class InactiveAccountException(AuthException):
    pass

class MaxTriesException(AuthException):
    pass

#constants for the recordset
SALT = 0
PASSWORD = 1
ACTIVATED = 2
TRIES = 3

def authenticate(email, password):
    if email is None:
       raise(NoEmailException() ) 
    if password is None:
       raise(NoPasswordException() ) 

    db = DB()
    users = db.get_user_by_email(email)
    if not users:
        raise(InvalidCredentialsException() )

    # constrains garantees that email is unique
    user = users[0]

    if user[ACTIVATED] is None:
        raise(InactiveAccountException() )

    if user[TRIES] >= settings.MAX_PWD_TRIES:
        raise(MaxTriesException() )
        
    m = sha1()
    m.update(user[SALT]+password)
     
    if m.hexdigest() == user[PASSWORD]:
        return db.successful_login(email)
    
    db.failed_login(email)
    raise(InvalidCredentialsException() )
    




