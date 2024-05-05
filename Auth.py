from selenium import webdriver
import os

from exceptions.Format import IncorrectFormat
from utils.navigation import get_webdriver
from constants import IMAGE_FORMATS
from utils.auth import *


class Account:
    def __init__(self, email: str) -> None:
        self.email = email
        self.auth = False

    @get_webdriver
    def login(self, driver: webdriver.Chrome, password: str):
        """
        Uses the Instagram UI to log in. It will require user interaction to get past CAPTCHAs and the sort.

        Args:
            password (str): password related to the account
        """
        # TODO: implement the functionality
        # Test code
        print(password)
        driver.get("https://www.google.com/")
        self.auth = True

    @check_auth
    @get_webdriver
    def post(self, driver: webdriver.Chrome, image_path: str):
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
        print(image_path)


# Usage
def test():
    account = Account("example@example.com")
    account.login("password123")
    account.post("path/to/image.jpg")


if __name__ == "__main__":
    test()
