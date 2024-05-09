from datetime import datetime
from selenium import webdriver
import time, random


def navigate(driver: webdriver.Chrome, url: str):
    """
    Navigates to a URL only if the URL is different to the current.
    """
    # No need to navigate if already on the same URL
    if driver.current_url == url:
        return

    driver.get(url)


def write(input, text, speed=5):
    """
    Types some text letter by letter at random intervals in an input field. This is done so the interaction feels more "human-like".

    Args:
        input (WebElement): The input to write in.
        text (str): Text to be written.
        speed (int): Divides the random float (from 0 to 1). The higher the number the faster it writes. Defaults to 5.
    """
    for letter in text:
        input.send_keys(letter)
        time.sleep(random.random() / speed)


def parse_instagram_date(time: str):
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
