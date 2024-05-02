from selenium import webdriver
from selenium_stealth import stealth


class WebDriver(type):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")

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
        return cls._instance
