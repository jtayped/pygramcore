from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
import pickle, os, time, random

from constants import *
from exceptions.auth import *
from exceptions.format import *
from utils.misc import write, navigate


def check_authorization(func):
    """
    Decorator that checks if the current account is logged in.

    Raises:
        NotAuthenticated: Raises when the current account is not logged in.
    """

    def wrapper(*args, **kwargs):
        logged_in = Account.is_logged_in()
        if not logged_in:
            raise NotAuthenticated()

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


class Navigator(type):
    def __new__(cls, name, bases, dct):
        """
        Wraps all relevant functions with _default_initialize_website to initialize the object's url and provide the current instance of the driver.
        """
        _initialize_website = dct.get(
            "_initialize_website", cls._default_initialize_website
        )
        for key, value in dct.items():
            if not key.startswith("__") and key != "_initialize_website":
                # Support for class methods that aren't the get_instance function.
                # This is done to prevent a recursion error, because the get_instance
                # function is the function used in _initialize_website (causing the error)
                if isinstance(value, classmethod) and key != "get_instance":
                    wrapped_method = classmethod(
                        cls.wrap_method(value.__func__, _initialize_website)
                    )
                    dct[key] = wrapped_method
                else:
                    if callable(value):
                        wrapped_method = cls.wrap_method(value, _initialize_website)
                        dct[key] = wrapped_method
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def wrap_method(method, before_all_method):
        def wrapped(self, *args, **kwargs):
            before_all_method(self)
            return method(self, *args, **kwargs)

        return wrapped

    @staticmethod
    def _default_initialize_website(self):
        """
        Provides the current instance of the driver to the object and navigates to the URL of it's object if there is any.
        """
        if not hasattr(self, "_driver"):
            self._driver = Account.get_instance()

        if hasattr(self, "url"):
            navigate(self._driver, self.url)


class Account(metaclass=Navigator):
    _driver: webdriver.Chrome
    _logged_in: bool = False

    @classmethod
    def get_instance(cls):
        """
        Returns the current instance of the webdriver.
        """
        if not hasattr(cls, "_driver"):
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
            raise InvalidFormat()

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
        share_btn.click()

    @classmethod
    def get_cookies(cls) -> list[dict]:
        """
        Returns the current cookies contained in the webdriver.

        Returns:
            list[dict]: list of cookies.
        """
        cookies = cls._driver.get_cookies()
        return cookies

    @classmethod
    def set_cookies(cls, cookies: list[dict]):
        """
        Removes all cookies and adds a list of new ones.

        Args:
            cookies (list[dict]): List of cookies from `.get_cookies()`.
        """
        cls._driver.delete_all_cookies()
        cls._driver.get(INSTAGRAM_URL)

        for cookie in cookies:
            cls._driver.add_cookie(cookie)

    @classmethod
    def load_cookies(cls, path: str):
        """
        Loads cookies from a file.

        Args:
            path (str): path to the file.
        """
        with open(path, "rb") as file:
            cookies = pickle.load(file)

        cls.set_cookies(cookies)
        cls._logged_in = bool(cookies)

    @classmethod
    def save_cookies(cls, path: str):
        """
        Saves the current cookies to a file.

        Args:
            path (str): path to the file.
        """
        with open(path, "wb") as file:
            pickle.dump(cls.get_cookies(), file)

    @classmethod
    def is_logged_in(cls) -> bool:
        """
        Returns:
            bool: Whether the account is logged in.
        """
        return cls._logged_in


def attempt_close_notification_dialog():
    driver = Account.get_instance()

    # Attempt to find the button
    driver.implicitly_wait(2)
    found = driver.find_elements(By.XPATH, '//button[text()="Not Now"]')
    driver.implicitly_wait(IMPLICIT_WAIT)

    # If found it shall click it
    if found:
        btn = found[0]
        btn.click()
