from driver import WebDriver


def check_navigation(func):
    def wrapper(url: str = None):
        # Get current instance of the driver
        instance = WebDriver.get_instance()

        # Check if currently on the same page
        if url and url != instance.current_url:
            instance.get(url)

        return instance

    return wrapper
