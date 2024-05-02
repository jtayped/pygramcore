from exceptions.Auth import AuthException


def check_auth(func):
    def wrapper(account, *args, **kwargs):
        if not account.auth:
            raise AuthException("User is not authenticated.")
        return func(account, *args, **kwargs)

    return wrapper
