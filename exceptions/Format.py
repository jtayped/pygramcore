from constants import IMAGE_FORMATS


class IncorrectFormat(Exception):
    """Raises when a file is not the correct format"""

    def __init__(
        self,
        message: str = "The file is not the correct format.",
        formats: list[str] = IMAGE_FORMATS,
        *args,
        **kwargs
    ) -> None:
        # TODO: instert the necessary formats in to the message
        super().__init__(message, *args)
