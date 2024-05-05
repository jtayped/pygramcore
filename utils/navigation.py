from driver import WebDriver
from constants import INSTAGRAM_URL


def get_webdriver(func):
    def wrapper(*args, **kwargs):
        # Get current instance of the driver
        instance = WebDriver.get_instance()

        return func(*args, instance, **kwargs)

    return wrapper
