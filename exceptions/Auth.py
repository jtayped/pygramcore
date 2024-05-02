class AuthException(Exception):
    """Raised when an account is not logged in."""

    def __init__(self, message: str = "Account not logged in.", *args, **kwargs):
        super().__init__(message, *args, **kwargs)
