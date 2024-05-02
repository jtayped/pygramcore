import os

from exceptions.Format import IncorrectFormat
from utils.navigation import check_navigation
from constants import IMAGE_FORMATS
from utils.auth import *


class Account:
    def __init__(self, email: str) -> None:
        self.email = email
        self.auth = False

    @check_navigation
    def login(self, password: str):
        """
        Uses the Instagram UI to log in. It will require user interaction to get past CAPTCHAs and the sort.

        Args:
            password (str): password related to the account
        """
        # TODO: implement the functionality
        # Test code
        self.auth = True

    @check_auth
    @check_navigation
    def post(self, image_path: str):
        """
        Posts a specific image to the account.

        Args:
            image_path (str): absolute path to the image
        """
        # Check if image is the correct format
        filename = os.path.basename(image_path)
        extension = filename.split(".")[-1]
        if extension not in IMAGE_FORMATS:
            raise IncorrectFormat()

        # TODO: posting functionality


# Usage
def test():
    account = Account("example@example.com")
    account.login("password123")
    account.post("path/to/image.jpg")


if __name__ == "__main__":
    test()
