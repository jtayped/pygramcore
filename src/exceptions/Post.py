class PostActionError(Exception):
    """Raised when action can't be taken on a post."""

    def __init__(self, message: str = "Unvalid action.", *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class PostError(Exception):
    """Unspecified post error"""

    def __init__(self, message: str, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
