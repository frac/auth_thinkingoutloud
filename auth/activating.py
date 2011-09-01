from dbutils import DB
import datetime
from datetime import timedelta

import settings

class ActivationException(Exception):
    pass

class UserNotFoundException(ActivationException):
    pass

class UserAlreadyActivatedException(ActivationException):
    pass

class UserExpiredException(ActivationException):
    pass

CREATED = 0
TOKEN = 1
ACTIVATED = 2

def activate(token):
    db = DB()
    users = db.get_user_by_token(token)
    if not users:
        raise(UserNotFoundException() )

    # constrain garantees that token is unique
    user = users[0]
    if not user[ACTIVATED] is None:
        raise(UserAlreadyActivatedException() )

    if user[CREATED] < str(datetime.datetime.now() - timedelta(days=settings.DAYS_TO_ACTIVATE)):
        raise(UserExpiredException() )

    db.activate_user(token)
    return True    
        



