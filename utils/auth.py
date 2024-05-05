from exceptions.Auth import AuthException
from auth import Account

def check_auth(func):
    def wrapper(*args, **kwargs):
        if not Account.is_logged_in():
            raise AuthException("User is not authenticated.")
        return func(*args, **kwargs)

    return wrapper
