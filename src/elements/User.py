from dataclasses import dataclass
from typing import Literal, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import time

from pygram import get_driver, check_authorization
from elements.Post import Post
from exceptions.User import *
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

    @check_authorization
    @get_driver()
    def is_private(self) -> bool:
        pass

    @check_authorization
    @get_driver()
    def follow(self) -> None:
        if self.is_following():
            raise UserActionError("You already follow this user.")

        follow_btn = self._driver.find_element(By.XPATH, '//div[text()="Follow"]')
        follow_btn.click()
        time.sleep(100)

        # Wait to load
        time.sleep(2)

    @check_authorization
    @get_driver()
    def unfollow(self) -> None:
        if not self.is_following():
            raise UserActionError("You don't follow this user.")

        self.open_user_dialog()
        # TODO

    @check_authorization
    @get_driver()
    def is_following(self):
        """
        Check whether you follow the user.

        Returns:
            bool: True if the user is followed, False if not.

        Raises:
            UserError: If it cannot determine if the user is followed or not.
        """

        self._driver.implicitly_wait(1)

        if self._driver.find_elements(By.XPATH, '//div[text()="Follow"]'):
            self._driver.implicitly_wait(10)
            return False
        elif self._driver.find_elements(By.XPATH, '//div[text()="Following"]'):
            self._driver.implicitly_wait(10)
            return True
        else:
            raise UserError("Cannot determine if user is followed or not.")

    @check_authorization
    @get_driver()
    def add_close_friend(self):
        """
        Adds user to close friends.
        """
        self.open_user_dialog()

        if self.is_close_friend():
            raise UserActionError("User is already a close friend.")

        close_friend_btn = self._driver.find_element(
            By.CSS_SELECTOR, "svg[aria-label='Close friend']"
        )
        close_friend_btn.click()

    @check_authorization
    @get_driver()
    def remove_close_friend(self):
        self.open_user_dialog()

        if not self.is_close_friend():
            raise UserActionError("User must be a close friend to be removed.")

        # TODO
        close_friend_btn = self._driver.find_element(
            By.CSS_SELECTOR, "svg[aria-label='Close friend']"
        )
        close_friend_btn.click()

    @check_authorization
    @get_driver()
    def is_close_friend(self):
        self.open_user_dialog()

        self._driver.implicitly_wait(2)

        # Check if not close friend
        elements = self._driver.find_elements(
            By.CSS_SELECTOR, "div[contains(text(), 'Add to Close Friends list')]"
        )
        if elements:
            self._driver.implicitly_wait(IMPLICIT_WAIT)
            return False

        # Check if already close friend
        elements = self._driver.find_elements(
            By.CSS_SELECTOR, "div[contains(text(), 'Close friend')]"
        )
        if elements:
            self._driver.implicitly_wait(IMPLICIT_WAIT)
            return True

        raise UserActionError("Couldn't find any indicator of close friends state...")

    @check_authorization
    @get_driver()
    def add_favourites(self):
        self.open_user_dialog()
        # TODO

    @check_authorization
    @get_driver()
    def mute(self, modes: List[Literal["posts", "stories"]]):
        self.open_user_dialog()
        # TODO

    @check_authorization
    @get_driver()
    def open_user_dialog(self):
        if not self.is_following():
            raise UserActionError("Can't open dialog if not following.")

        # Check if it's not already open
        if self.user_dialog_open():
            return

        # Open the dialog
        unfollow_btn = self._driver.find_element(By.XPATH, '//div[text()="Following"]')
        unfollow_btn.click()

    def user_dialog_open(self) -> bool:
        # Check for elements that comply with the CSS selector
        elements = self._driver.find_elements(
            By.CSS_SELECTOR,
            "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xyamay9.x1pi30zi.x1l90r2v.x1swvt13.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1 > span",
        )

        # Return whether any elements have been found
        is_open = bool(elements)
        return is_open

    @get_driver()
    def get_total_posts(self) -> int:
        posts_span, _, _ = self._driver.find_elements(By.CSS_SELECTOR, "span._ac2a")
        posts_str = posts_span.find_element(By.CSS_SELECTOR, "span").text

        # Remove the commas and convert to integer
        followers = int(posts_str.replace(",", ""))
        return followers

    @get_driver()
    def get_followers(self) -> int:
        # Gets the string value (e.g. "156,204")
        _, followers_span, _ = self._driver.find_elements(By.CSS_SELECTOR, "span._ac2a")
        followers_str = followers_span.get_property("title")

        # Remove the commas and convert to integer
        followers = int(followers_str.replace(",", ""))
        return followers

    @get_driver()
    def get_following(self) -> int:
        _, _, following_span = self._driver.find_elements(By.CSS_SELECTOR, "span._ac2a")
        following_str = following_span.find_element(By.CSS_SELECTOR, "span").text

        # Remove the commas and convert to integer
        followers = int(following_str.replace(",", ""))
        return followers

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
