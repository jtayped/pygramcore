from selenium import webdriver
from selenium.webdriver.common.by import By

import os, time

from exceptions.Format import IncorrectFormat
from utils.navigation import *
from constants import *


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
        self.driver: webdriver.Chrome = None

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

    @get_webdriver(INSTAGRAM_LOGIN_URL)
    @handle_cookies_dialog
    def login(self):
        """
        Uses the Instagram UI to log in. It will require user interaction to get past CAPTCHAs and the sort.
        Returns:
            list[dict]: list of cookies.
        """
        # Write email
        email_input = self.driver.find_element(
            By.CSS_SELECTOR, "#loginForm > div > div:nth-child(1) > div > label > input"
        )
        email_input.send_keys(self._email)

        # Write password
        password_input = self.driver.find_element(
            By.CSS_SELECTOR, "#loginForm > div > div:nth-child(2) > div > label > input"
        )
        password_input.send_keys(self._password)

        # Login
        login_btn = self.driver.find_element(
            By.CSS_SELECTOR, "#loginForm > div > div:nth-child(3) > button"
        )
        login_btn.click()

        time.sleep(100)
        # Return cookies after logging in
        self._cookies = self.driver.get_cookies()
        return self._cookies

    @get_webdriver(INSTAGRAM_URL)
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


def test():
    acc = Account("jtayped@gmail.com", "Tayped123+")
    acc.login()

if __name__ == "__main__":
    test()