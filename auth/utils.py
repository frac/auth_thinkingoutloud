import random
import string


def create_token(size=32):
    """
    Uses only letters and numbers for the salt.
    """
    available_chars = string.letters + string.digits 
    return ''.join( random.choice(available_chars) for _ in xrange(size))

