from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

from pygram import get_driver
from elements.Post import Post
from constants import *


@dataclass
class User:
    """
    Represents an Instagram user.

    Args:
        name (str): Username of the user.
    """

    name: str

    def __post_init__(self):
        self._driver: webdriver.Chrome = None
        self.url = f"{INSTAGRAM_URL}/{self.name}/"

    @get_driver()
    def is_private(self) -> bool:
        pass

    @get_driver()
    def follow(self) -> None:
        pass

    @get_driver()
    def unfollow(self) -> None:
        pass

    @get_driver()
    def get_followers(self) -> int:
        pass

    @get_driver()
    def get_following(self) -> int:
        pass

    @get_driver()
    def send_dm(self, message: str) -> None:
        pass

    @get_driver()
    def get_posts(self, reels=True, limit=10) -> list[Post]:
        # Go to user instagram page
        self._driver.get(self.url)

        css_selector = "a[href^='/p/']"
        if reels:
            css_selector += ",a[href^='/reel/']"

        posts = []

        # Scroll down to load posts
        while len(posts) < limit:
            # Scroll down
            self._driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)

            # Wait for new posts to load
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
            )

            # Get all posts
            post_elements = self._driver.find_elements(By.CSS_SELECTOR, css_selector)

            # Add new posts to the list
            for post_element in post_elements:
                href = post_element.get_attribute("href")
                path = urlparse(href).path
                id = path.split("/")[2]

                post = Post(id)
                posts.append(post)

            # If no new posts loaded, break the loop
            if len(post_elements) == 0:
                break

        return posts[:limit]
