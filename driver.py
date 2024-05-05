from selenium import webdriver
from selenium_stealth import stealth


class WebDriver(type):
    """
    Singleton for the main instance of the driver. Use `WebDriver.get_instance()` to get the current instance of the driver.
    """
    _instance = None

    @classmethod
    def get_instance(cls):
        """
        Returns the current instance of the webdriver.
        """
        if cls._instance is None:
            options = webdriver.ChromeOptions()

            cls._instance = webdriver.Chrome(options=options)
            stealth(
                cls._instance,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )

            # Set initial implicit wait
            cls._instance.implicitly_wait(10)

        return cls._instance
