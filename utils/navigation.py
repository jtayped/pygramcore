from driver import WebDriver
from constants import INSTAGRAM_URL


def get_webdriver(func):
    def wrapper(account, *args, **kwargs):
        # Get current instance of the driver
        instance = WebDriver.get_instance()
        account.driver = instance

        # Add cookies to the driver if any
        if account.cookies:
            current_cookies = instance.get_cookies()

            for cookie in account.cookies:
                # Check if they have been added already
                if cookie not in current_cookies:
                    instance.add_cookie(cookie)

        return func(account, *args, **kwargs)

    return wrapper
