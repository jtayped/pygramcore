from driver import WebDriver
from constants import IMPLICIT_WAIT


def get_webdriver(url: str = None):
    """
    Inserts the current instance of the webdriver in the class instance.

    Args:
        url (str): Initial URL to go to.

    Usage:
    ```
    @get_webdriver("https://google.com")
    def your_function(driver):
        ...

    your_function()
    ```
    """

    def decorator(func):
        def wrapper(account, *args, **kwargs):
            # Get current instance of the driver
            instance = WebDriver()

            # Navigate to url if specified
            if url:
                instance.get(url)

            account.driver = instance

            # Add cookies to the driver if any
            if account.get_cookies():
                current_cookies = instance.get_cookies()

                for cookie in account.cookies:
                    # Check if they have been added already
                    if cookie not in current_cookies:
                        instance.add_cookie(cookie)

            return func(account, *args, **kwargs)

        return wrapper

    return decorator


def handle_cookies_dialog(func):
    def wrapper(*args, **kwargs):
        # Get current instance of the driver
        driver = WebDriver()

        # Set implicit wait to lower value
        driver.implicitly_wait(2)

        try:
            # Attempt to decline cookies
            btn = driver.find_element("button._a9--._ap36._a9_1")
            btn.click()
        except:
            pass
        finally:
            driver.implicitly_wait(IMPLICIT_WAIT)

        # Run function being decorated
        func(*args, **kwargs)

    return wrapper
