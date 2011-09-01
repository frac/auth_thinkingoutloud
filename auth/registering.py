from hashlib import sha1
import re

from dbutils import DB
from notifications import send_new_user_notification
from utils import create_token

def get_salt():
    return create_token()
    


"""
A note about email validation:
We accept "a" to "z", 0 to 9 and "._%-" in the user part of the field
for the domain we accept "a" to "z", 0 to 9 and ".-"
the tld must be 2 to 4 letters to support things like ".info"
space is invalid in any place
and also no support for non ascii domains.
"""
EMAIL_CHECK = re.compile(r"^[a-z0-9._%-]+@[a-z0-9.-]+\.[a-z]{2,4}$", re.IGNORECASE)



def register(email, password):
    """
    generates a random salt, salts the password and saves
    """
    if not email:
        return (False, "Empty email") 

    if not password:
        return (False, "Empty password") 

    if not EMAIL_CHECK.match(email):
        return (False, "Invalid email") 

    password = password.strip()
    if len(password) < 6:
        return (False, "Invalid password") 

    salt = get_salt()
    token = create_token().lower()
    
    m = sha1()
    m.update(salt + password)
    res = DB().create_user(email, salt, m.hexdigest(), token)
    if res[0]:
        send_new_user_notification(email, token)
    return res




