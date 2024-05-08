from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
import pickle, os, time, random

from constants import *
from exceptions.Auth import AuthException
from exceptions.Format import IncorrectFormat
from utils.misc import write, navigate


def check_authorization(func):
    def wrapper(*args, **kwargs):
        logged_in = Account.is_logged_in()
        if not logged_in:
            raise AuthException("Account is not authenticated.")

        value = func(*args, **kwargs)
        return value

    return wrapper


def init_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(options=options)
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    driver.implicitly_wait(IMPLICIT_WAIT)

    return driver


class Account:
    _driver = init_driver()
    _logged_in = False

    def __new__(cls):
        """
        Returns the current instance of the webdriver.
        """
        if cls._driver is None:
            driver = init_driver()
            cls._driver = driver

        return cls._driver

    @classmethod
    def login(cls, email: str | list[dict], password: str = None) -> list[dict] | None:
        """
        Uses the Instagram UI to log in. It will require user interaction to get past CAPTCHAs and the sort.

        Returns:
            list[dict]: list of cookies.
        """
        # Check if email/password exist
        if not (email and password):
            raise ValueError(
                "Missing email or password. If no cookies are given, please insert both."
            )

        # Write email
        email_input = cls._driver.find_element(
            By.CSS_SELECTOR, "#loginForm > div > div:nth-child(1) > div > label > input"
        )
        write(email_input, email)

        # Write password
        password_input = cls._driver.find_element(
            By.CSS_SELECTOR, "#loginForm > div > div:nth-child(2) > div > label > input"
        )
        write(password_input, password)

        # Login
        login_btn = cls._driver.find_element(
            By.CSS_SELECTOR, "#loginForm > div > div:nth-child(3) > button"
        )
        login_btn.click()

        # Wait till fully logged in
        time.sleep(5)

        # Update value
        cls._logged_in = True

        # Save and return cookies after logging in
        current_cookies = cls._driver.get_cookies()
        cls.set_cookies(current_cookies)
        return current_cookies

    @classmethod
    @check_authorization
    def post(cls, media_path: str, caption: str = None):
        """
        Posts a specific image to the account.
        Args:
            media_path (str): absolute path to the image
        """
        # Make the path absolute
        media_path = os.path.abspath(media_path)

        # Check if image is the correct format
        _, extension = os.path.splitext(media_path)
        if extension[1:] not in MEDIA_FORMATS:
            raise IncorrectFormat()

        # Open create dialog
        create_button = cls._driver.find_element(
            By.CSS_SELECTOR,
            "svg[aria-label='New post']",
        )
        create_button.click()

        # Add file to the input
        file_input = cls._driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(media_path)

        # Click 'Next' next button twice
        for _ in range(2):
            # It requires to be found each iteration due to the "StaleElementReferenceException"
            next_btn = cls._driver.find_element(
                By.CSS_SELECTOR,
                "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div > div > div > div._ap97 > div > div > div > div._ac7b._ac7d > div",
            )
            next_btn.click()
            time.sleep(random.random())

        # Write caption if specified
        if caption:
            caption_input = cls._driver.find_element(
                By.CSS_SELECTOR, "div[aria-label='Write a caption...']"
            )
            write(caption_input, caption)

        # Click 'Share' button
        share_btn = cls._driver.find_element(
            By.CSS_SELECTOR,
            "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div > div > div > div._ap97 > div > div > div > div._ac7b._ac7d > div",
        )
        next_btn.click()

    @classmethod
    def get_cookies(cls):
        cookies = cls._driver.get_cookies()
        return cookies

    @classmethod
    def set_cookies(cls, cookies: list[dict]):
        cls._driver.delete_all_cookies()
        cls._driver.get(INSTAGRAM_URL)

        for cookie in cookies:
            cls._driver.add_cookie(cookie)

    @classmethod
    def load_cookies(cls, path: str):
        with open(path, "rb") as file:
            cookies = pickle.load(file)

        cls.set_cookies(cookies)
        cls._logged_in = bool(cookies)

    @classmethod
    def save_cookies(cls, path: str):
        # TODO: add argument to add custom cookies (which is not required)
        with open(path, "wb") as file:
            pickle.dump(cls.get_cookies(), file)

    @classmethod
    def is_logged_in(cls):
        return cls._logged_in


class Navigator:
    def __init__(self) -> None:
        self._driver = Account()
