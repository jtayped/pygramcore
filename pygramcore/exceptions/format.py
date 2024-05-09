from constants import MEDIA_FORMATS


class InvalidFormat(Exception):
    def __init__(self) -> None:
        super().__init__(
            f"Please insert media of an appropriate format ({', '.join(MEDIA_FORMATS)})."
        )
