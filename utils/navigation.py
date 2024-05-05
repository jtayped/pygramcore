from driver import WebDriver
from constants import INSTAGRAM_URL


def get_webdriver(func):
    def wrapper(self, *args, **kwargs):
        # Get current instance of the driver
        instance = WebDriver.get_instance()

        return func(self, instance, *args, **kwargs)

    return wrapper
