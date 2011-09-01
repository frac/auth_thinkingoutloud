from dbutils import DB

def authorize(auth_token):
    if auth_token is None:
        return False
    db = DB()
    users = db.get_user_by_auth_token(auth_token)
    if not users:
        return False

    return True
    # constrains garantees that email is unique
    user = users[0]
    

