import os
from exceptions.Format import IncorrectFormat
from utils.navigation import get_webdriver
from constants import IMAGE_FORMATS


class Account:
    """
    Represents an Instagram account.
    """

    _cookies = None
    _logged_in = False

    @classmethod
    def get_cookies(cls):
        return cls._cookies

    @classmethod
    def set_cookies(cls, cookies):
        cls._cookies = cookies

    @classmethod
    def is_logged_in(cls):
        return cls._logged_in

    @classmethod
    @get_webdriver
    def login(cls, email: str, password: str):
        """
        Uses the Instagram UI to log in. It will require user interaction to get past CAPTCHAs and the sort.

        Args:
            password (str): password related to the account.

        Returns:
            list[dict]: list of cookies.
        """
        # TODO: implement the functionality
        cls._logged_in = True  # test

        # Return cookies after logging in
        cookies = cls.driver.get_cookies()
        return cookies

    @get_webdriver
    def post(self, image_path):
        """
        Posts a specific image to the account.

        Args:
            image_path (str): absolute path to the image
        """
        # Check if image is the correct format
        _, extension = os.path.splitext(image_path)
        if extension[1:] not in IMAGE_FORMATS:
            raise IncorrectFormat()

        # TODO: posting functionality


# Usage
def test():
    account = Account()
    account.login("example@example.com", "password123")
    account.post("path/to/image.jpg")


if __name__ == "__main__":
    test()
