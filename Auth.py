from selenium import webdriver
import os

from exceptions.Format import IncorrectFormat
from exceptions.Auth import AuthException
from utils.navigation import get_webdriver
from constants import IMAGE_FORMATS


class Account:
    """
    Represents an Instagram account.
    """

    _instance = None

    def __init__(self, email: str, password: str):
        if Account._instance is not None:
            raise RuntimeError("Cannot instantiate more than one Account.")
        Account._instance = self
        self._email = email
        self._password = password
        self._cookies = None
        self._logged_in = False
        self.driver = None

    @classmethod
    def get_instance(cls):
        """
        Returns the current instance of the account.
        """
        return cls._instance

    def get_cookies(self):
        return self._cookies

    def set_cookies(self, cookies):
        self._cookies = cookies

    def is_logged_in(self):
        return self._logged_in

    @get_webdriver
    def login(self):
        """
        Uses the Instagram UI to log in. It will require user interaction to get past CAPTCHAs and the sort.
        Returns:
            list[dict]: list of cookies.
        """
        # TODO: implement the functionality
        self._logged_in = True  # test

        # Return cookies after logging in
        self._cookies = self.driver.get_cookies()
        return self._cookies

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
