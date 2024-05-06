from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import List, Dict, Union
import os
import time
import random

from exceptions.Format import IncorrectFormat
from utils.navigation import *
from constants import *


class Account:
    """
    Represents an instagram account.

    Args:
        email_or_cookies (Union[str, List[Dict[str, str]]]):
            Either the email address of the account as a string or
            a list of cookies as dictionaries. If email is provided,
            the `password` argument can be optionally provided.
        password (str, optional):
            The password of the account. Required if `email_or_cookies`
            is an email address. Defaults to None.

    Raises:
        RuntimeError:
            If an attempt is made to instantiate more than one Account object.
        ValueError:
            If the `email_or_cookies` argument is neither a string nor a list.
    """

    _instance = None

    def __init__(
        self, email_or_cookies: Union[str, List[Dict[str, str]]], password: str = None
    ):
        if Account._instance is not None:
            raise RuntimeError("Cannot instantiate more than one Account.")
        Account._instance = self

        if isinstance(email_or_cookies, str):
            self._email = email_or_cookies
            self._password = password
            self._cookies = []
        elif isinstance(email_or_cookies, list):
            self._email = None
            self._password = None
            self._cookies = email_or_cookies
        else:
            raise ValueError("Invalid argument type for email_or_cookies.")

        self._logged_in = bool(self._cookies)
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
        self.write(email_input, self._email)

        # Write password
        password_input = self.driver.find_element(
            By.CSS_SELECTOR, "#loginForm > div > div:nth-child(2) > div > label > input"
        )
        self.write(password_input, self._password)

        # Login
        login_btn = self.driver.find_element(
            By.CSS_SELECTOR, "#loginForm > div > div:nth-child(3) > button"
        )
        login_btn.click()

        # Wait till fully logged in
        time.sleep(5)

        # Update value
        self._logged_in = True

        # Return cookies after logging in
        self._cookies = self.driver.get_cookies()
        return self._cookies

    @get_webdriver(INSTAGRAM_URL)
    def post(self, image_path: str, caption: str = None):
        """
        Posts a specific image to the account.
        Args:
            image_path (str): absolute path to the image
        """
        # Check if image is the correct format
        _, extension = os.path.splitext(image_path)
        if extension[1:] not in MEDIA_FORMATS:
            raise IncorrectFormat()

        # Open create dialog
        create_button = self.driver.find_element(
            By.CSS_SELECTOR,
            "svg[aria-label='New post']",
        )
        create_button.click()

        # Add file to the input
        file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(image_path)

        # Click 'Next' next button twice
        for _ in range(2):
            # It requires to be found each iteration due to the "StaleElementReferenceException"
            next_btn = self.driver.find_element(
                By.CSS_SELECTOR,
                "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div > div > div > div._ap97 > div > div > div > div._ac7b._ac7d > div",
            )
            next_btn.click()
            time.sleep(random.random())

        # Write caption if specified
        if caption:
            caption_input = self.driver.find_element(
                By.CSS_SELECTOR, "div[aria-label='Write a caption...']"
            )
            self.write(caption_input, caption)

        # Click 'Share' button
        share_btn = self.driver.find_element(
            By.CSS_SELECTOR,
            "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div > div > div > div._ap97 > div > div > div > div._ac7b._ac7d > div",
        )
        # next_btn.click()

    def write(self, input, text, speed=3):
        """
        Types some text letter by letter at random intervals in an input field. This is done so the interaction feels more "human-like".

        Args:
            input (WebElement): The input to write in.
            text (str): Text being written.
            speed (int): Divides the random float (from 0 to 1). The higher the number the faster it writes.
        """
        for letter in text:
            input.send_keys(letter)
            time.sleep(random.random() / speed)
