from selenium import webdriver
from dataclasses import dataclass
import os

from exceptions.Format import IncorrectFormat
from utils.navigation import get_webdriver
from constants import IMAGE_FORMATS
from utils.auth import *


@dataclass
class Account:
    """
    Represents an Instagram account.

    Args:
        email (str): Email linked to the Instagram account.
        cookies (list[dict]): Cookies associated with the account.
    """

    email: str
    cookies: list[dict] = None

    def __post_init__(self):
        self.driver: webdriver.Chrome = None
        self._logged_in = True if self.cookies else False

    def is_logged_in(self):
        return self._logged_in
    
    @get_webdriver
    def login(self, password: str) -> list[dict]:
        """
        Uses the Instagram UI to log in. It will require user interaction to get past CAPTCHAs and the sort.

        Args:
            password (str): password related to the account.

        Returns:
            list[dict]: list of cookies.
        """
        # TODO: implement the functionality
        self._logged_in = True # test

        # Return cookies after logging in
        cookies = self.driver.get_cookies()
        return cookies

    @check_auth
    @get_webdriver
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
    account = Account(
        "example@example.com",
    )
    account.login("password123")
    account.post("path/to/image.jpg")


if __name__ == "__main__":
    test()
