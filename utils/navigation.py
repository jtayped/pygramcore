from driver import WebDriver


def get_webdriver(url: str):
    """
    Passes the current instance of the webdriver in the arguments.

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
