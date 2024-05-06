from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        @disallow_notifications
        def wrapper(account, *args, **kwargs):
            # Get current instance of the driver
            instance = WebDriver()

            # Navigate to url if specified
            if url:
                instance.get(url)

            account.driver = instance

            # Add cookies to the driver if any
            account_cookies = account.get_cookies()
            if account_cookies:
                current_cookies = instance.get_cookies()

                for cookie in account_cookies:
                    # Check if they have been added already
                    if cookie not in current_cookies:
                        print("aa")
                        instance.add_cookie(cookie)

                # Refresh page to effectuate cookies
                instance.refresh()

            value = func(account, *args, **kwargs)
            return value

        return wrapper

    return decorator


def handle_cookies_dialog(func):
    def wrapper(*args, **kwargs):
        # Get current instance of the driver
        driver = WebDriver()

        # Attempt to click the cookies dialog if found
        # If not, it shall pass
        try:
            btn = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe.x5yr21d.x19onx9a > div > button._a9--._ap36._a9_1",
                    )
                )
            )
            btn.click()
        except:
            pass

        # Run function being decorated
        value = func(*args, **kwargs)
        return value

    return wrapper


def disallow_notifications(func):
    """
    Clicks "Not Now" when Instagram asks for notification access. This decorator should be placed on functions that login the account.
    """

    def wrapper(*args, **kwargs):
        # Run function being decorated
        value = func(*args, **kwargs)

        # Get current instance of the driver
        driver = WebDriver()

        # Attempt to disallow notifications
        try:
            btn = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div._a9-z > button._a9--._ap36._a9_1",
                    )
                )
            )
            btn.click()
        except:
            pass

        return value

    return wrapper
