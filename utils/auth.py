from exceptions.Auth import AuthException


def check_auth(func):
    def wrapper(account, *args, **kwargs):
        if not account.is_logged_in():
            raise AuthException("User is not authenticated.")
        return func(account, *args, **kwargs)

    return wrapper
