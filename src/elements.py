from dataclasses import dataclass
from typing import Literal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from urllib.parse import urlparse
from datetime import datetime

from pygram import Navigator, check_authorization
from exceptions.user import *
from exceptions.post import *
from utils.misc import *
from constants import *


def user_dialog_action(func):
    """
    Decorator function that opens and closes the user dialog. The user dialog is where you can take actions on a user, such as: unfollowing, adding or removing from close friends, etc...
    """

    def wrapper(user: "User", *args, **kwargs):
        if not user.is_following():
            raise UserNotFollowed(user.name)

        # Check if it's not already open
        if user.user_dialog_open():
            return

        # Open the dialog
        dialog_btn = user._driver.find_element(By.XPATH, '//div[text()="Following"]')
        dialog_btn.click()

        # Perform function being decorated
        value = func(user, *args, **kwargs)

        # Attempt to close the user dialog, some actions
        # close the dialog automatically (e.g. unfollowing)
        try:
            close_btn = user._driver.find_element(
                By.CSS_SELECTOR,
                "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div > div.x78zum5.xds687c.x1iorvi4.x1sxyh0.xjkvuk6.xurb0ha.x10l6tqk.x1vjfegm > div > div > svg",
            )
            close_btn.click()
        except:
            pass
        finally:
            user._driver.implicitly_wait(IMPLICIT_WAIT)

        return value

    return wrapper


@dataclass
class User(metaclass=Navigator):
    """
    Represents an Instagram user.

    Args:
        name (str): Username of the user.
    """

    name: str

    def __post_init__(self):
        self._driver: webdriver.Chrome
        self.url = f"{INSTAGRAM_URL}/{self.name}/"

    @check_authorization
    def is_private(self) -> bool:
        pass

    @check_authorization
    def follow(self) -> None:
        """
        Follows the user with the current account logged in.

        Raises:
            UserAlreadyFollowed: Raises when the user is already followed. Use `.is_followed()` to check if followed.
            NotAuthenticated: Raises when the current account is not logged in.
        """
        if self.is_following():
            raise UserAlreadyFollowed(self.name)

        follow_btn = self._driver.find_element(By.XPATH, '//div[text()="Follow"]')
        follow_btn.click()

    @check_authorization
    @user_dialog_action
    def unfollow(self) -> None:
        """
        Unfollows the user with the current account logged in.

        Raises:
            UserNotFollowed: Raises when the user is not followed. Use `.is_followed()` to check if followed.
            NotAuthenticated: Raises when the current account is not logged in.
        """
        if not self.is_following():
            raise UserNotFollowed(self.name)

        unfollow_btn = self._driver.find_element(
            By.CSS_SELECTOR,
            "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div > div:nth-child(8)",
        )
        unfollow_btn.click()

    @check_authorization
    def is_following(self):
        """
        Check whether you follow the user.

        Returns:
            bool: True if the user is followed, False if not.

        Raises:
            NotAuthenticated: Raises when the current account is not logged in.
        """

        self._driver.implicitly_wait(1)

        if self._driver.find_elements(By.XPATH, '//div[text()="Follow"]'):
            self._driver.implicitly_wait(10)
            return False
        elif self._driver.find_elements(By.XPATH, '//div[text()="Following"]'):
            self._driver.implicitly_wait(10)
            return True

    @check_authorization
    @user_dialog_action
    def add_close_friend(self):
        """
        Adds the user to the current account's close friends.

        Raises:
            UserCloseFriend: Raises when the user is already a close friend.
            NotAuthenticated: Raises when the current account is not logged in.
        """
        if self.is_close_friend():
            raise UserCloseFriend(self.name)

        close_friend_btn = self._driver.find_element(
            By.CSS_SELECTOR, "svg[aria-label='Close friend']"
        )
        close_friend_btn.click()

    @check_authorization
    @user_dialog_action
    def remove_close_friend(self):
        """
        Removes the user from the current account's close friends.

        Raises:
            UserNotCloseFriend: Raises when the user is not close friends already.
            NotAuthenticated: Raises when the current account is not logged in.
        """
        if not self.is_close_friend():
            raise UserNotCloseFriend(self.name)

        close_friend_btn = self._driver.find_element(
            By.CSS_SELECTOR, "svg[aria-label='Close friend']"
        )
        close_friend_btn.click()

    @check_authorization
    @user_dialog_action
    def is_close_friend(self) -> bool:
        """
        Checks if the user is a close friend.

        Returns:
            bool: Whether the user is a close friend

        Raises:
            NotAuthenticated: Raises when the current account is not logged in.
        """
        self._driver.implicitly_wait(2)

        # Check if not close friend
        elements = self._driver.find_elements(
            By.XPATH, '//svg[contains(@class,"x5n08af")][@width="16"]'
        )

        if elements:
            self._driver.implicitly_wait(IMPLICIT_WAIT)
            return False

        # Check if already close friend
        elements = self._driver.find_elements(
            By.XPATH,
            '//svg[contains(@class,"x1g9anri")]',
        )

        if elements:
            self._driver.implicitly_wait(IMPLICIT_WAIT)
            return True

    @check_authorization
    @user_dialog_action
    def mute(
        self,
        *modes: Literal["posts", "stories"],
    ):
        """
        Mutes the user's posts and/or stories. It is important to note that this function only enables the option, and can't disable it.

        Args:
            modes ("posts" and/or "stories"): Modes to mute, which can be posts and/or stories.

        Usage:
        ```python
        user = User("username")
        user.mute("stories", "posts")
        ```

        Raises:
            ValueError: if a mode in the arguments does not exist.
            NotAuthenticated: Raises when the current account is not logged in.
        """
        if isinstance(modes[0], str):
            modes = list(modes)

        if not all(mode in ["posts", "stories"] for mode in modes):
            raise ValueError("This mute mode does not exist!")

        mute_menu = self._driver.find_element(
            By.CSS_SELECTOR,
            "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div > div:nth-child(6)",
        )
        mute_menu.click()

        mute_btns = self._driver.find_elements(
            By.XPATH,
            '//input[@dir="ltr"]',
        )

        # Associate mute modes to indexes of the options on the menu
        mode_indexes = {"posts": 0, "stories": 1}
        for mode in modes:
            mute_btn_idx = mode_indexes[mode]
            mute_btn = mute_btns[mute_btn_idx]

            # Check if the mode is checked already
            is_checked = mute_btn.get_attribute("aria-checked")
            if is_checked.lower() == "false":
                mute_btn.click()

        # Submit options
        submit_btn = self._driver.find_element(
            By.CSS_SELECTOR,
            "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1y1aw1k.x1sxyh0.xwib8y2.xurb0ha.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div",
        )
        submit_btn.click()

    def user_dialog_open(self) -> bool:
        """
        Checks if the user dialog is open. The user dialog refers to the menu that opens when clicking the 'Following' button in the user page.

        Returns:
            bool: Whether the dialog is open
        """
        elements = self._driver.find_elements(
            By.CSS_SELECTOR,
            "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xyamay9.x1pi30zi.x1l90r2v.x1swvt13.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1 > span",
        )

        # Return whether any elements are in the list (found or not)
        is_open = bool(elements)
        return is_open

    def get_total_posts(self) -> int:
        """
        Get the user's total amount of posts.

        Returns:
            int: total posts
        """
        posts_span, _, _ = self._driver.find_elements(By.CSS_SELECTOR, "span._ac2a")
        posts_str = posts_span.find_element(By.CSS_SELECTOR, "span").text

        # Remove the commas and convert to integer
        followers = int(posts_str.replace(",", ""))
        return followers

    def get_followers(self) -> int:
        """
        Get the user's total amount of followers

        Returns:
            int: total followers
        """
        # Gets the string value (e.g. "156,204")
        _, followers_span, _ = self._driver.find_elements(By.CSS_SELECTOR, "span._ac2a")
        followers_str = followers_span.get_property("title")

        # Remove the commas and convert to integer
        followers = int(followers_str.replace(",", ""))
        return followers

    def get_following(self) -> int:
        """
        Get the amount of people the user follows.

        Returns:
            int: total following
        """
        _, _, following_span = self._driver.find_elements(By.CSS_SELECTOR, "span._ac2a")
        following_str = following_span.find_element(By.CSS_SELECTOR, "span").text

        # Remove the commas and convert to integer
        followers = int(following_str.replace(",", ""))
        return followers

    def send_dm(self, message: str) -> None:
        pass  # TODO

    def get_posts(self, reels=True, limit=25) -> list["Post"]:
        """
        Get a list of posts from the user's account.

        Args:
            reels (bool, optional): Whether to include reels or not. Defaults to True.
            limit (int, optional): Limits the amount of posts to retrieve. Defaults to 25.

        Returns:
            list[Post]: List of post objects

        Usage:
        ```python
        # Fetch username's posts
        user = User("username")
        posts = user.get_posts()

        # Like his first three posts
        for post in posts[:3]:
            post.like()
        ```
        """
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


@dataclass
class Post(metaclass=Navigator):
    id: str

    def __post_init__(self):
        self._driver: webdriver.Chrome
        self.url = f"{INSTAGRAM_URL}/p/{self.id}"

    @check_authorization
    def like(self) -> None:
        """
        Likes the post.

        Raises:
            PostLiked: Raises when the post is already liked.
            NotAuthenticated: Raises when the current account is not logged in.
        """
        if self.is_liked():
            raise PostLiked()

        likeButton = self._driver.find_element(
            By.CSS_SELECTOR, "div.x78zum5 > span.xp7jhwk > div"
        )
        likeButton.click()
        likeButton.click()

    @check_authorization
    def unlike(self) -> None:
        """
        Unlikes the post.

        Raises:
            PostNotLiked: Raises when the post is not liked already.
            NotAuthenticated: Raises when the current account is not logged in.
        """
        if not self.is_liked():
            raise PostNotLiked()

        likeButton = self._driver.find_element(
            By.CSS_SELECTOR, "div.x78zum5 > span.xp7jhwk > div"
        )
        likeButton.click()

    @check_authorization
    def is_liked(self) -> bool:
        """
        Checks whether the post is liked.

        Returns:
            bool: whether the post is liked.

        Raises:
            NotAuthenticated: Raises when the current account is not logged in.
        """

        self._driver.implicitly_wait(1)

        if self._driver.find_elements(
            By.CSS_SELECTOR, "svg[aria-label='Like'][width='24']"
        ):
            self._driver.implicitly_wait(10)
            return False
        elif self._driver.find_elements(
            By.CSS_SELECTOR, "svg[aria-label='Unlike'][width='24']"
        ):
            self._driver.implicitly_wait(10)
            return True

    @check_authorization
    def get_total_likes(self) -> int:
        """
        Returns the total amount of likes.

        Returns:
            int: Number of likes

        Raises:
            NotAuthenticated: Raises when the current account is not logged in.
        """
        likes_element = self._driver.find_element(
            By.XPATH,
            '//section[@class="x12nagc"]//span[@class="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"]',
        )
        total_likes = int(likes_element.text.replace(",", ""))
        return total_likes

    @check_authorization
    def get_liked_by(self, limit=25) -> list:
        # Open likes dialog
        likes_element = self._driver.find_element(
            By.XPATH,
            '//section[@class="x12nagc"]//span[@class="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"]',
        )
        likes_element.click()

        # Initialize list to store unique users
        users = []

        while True:
            try:
                # Find the user list container
                user_list = self._driver.find_element(
                    By.CSS_SELECTOR,
                    "div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x6ikm8r.x10wlt62.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div",
                )

                # Find all the username elements
                username_elements = user_list.find_elements(
                    By.CSS_SELECTOR, "span._ap3a._aaco._aacw._aacx._aad7._aade"
                )
            except StaleElementReferenceException:
                # Wait for the list of users to load
                time.sleep(1)

                # Retry if stale element exception occurs
                continue

            # Extract usernames and create User objects
            new_users = [User(element.text) for element in username_elements]

            # Add unique users to the list
            for user in new_users:
                if user.name not in [u.name for u in users]:
                    users.append(user)

            # Scroll to the last user element to load more users
            if new_users:
                last_user = username_elements[-1]
                self._driver.execute_script(
                    "arguments[0].scrollIntoView(true);", last_user
                )

            # Check if the limit is reached or no new users are loaded
            if len(users) >= limit or not new_users:
                break

        # Close the dialog by refreshing the page
        self._driver.refresh()

        # Return the necessary number of users within the limit
        return users[:limit]

    @check_authorization
    def get_images(self) -> list[str]:
        """
        Gets list of images from the post.

        Returns:
            list[str]: List of image URLs

        Raises:
            NotAuthenticated: Raises when the current account is not logged in.
        """
        image_elements = self._driver.find_elements(By.CSS_SELECTOR, "li._acaz")

        urls = []
        for element in image_elements:
            image_element = element.find_element(By.TAG_NAME, "img")
            image_url = image_element.get_attribute("src")
            urls.append(image_url)

        return urls

    @check_authorization
    def comment(self, text: str):
        """
        Comments on the post.

        Args:
            text (str): The comment.

        Raises:
            CannotComment: Whether you can comment.
            NotAuthenticated: Raises when the current account is not logged in.
        """
        # TODO: when comment implementation done continue...
        if not self.can_comment():
            raise CannotComment()

        # Find form and write the comment text
        form_element = self._driver.find_element(By.TAG_NAME, "form")

        # The textarea changes when selecting it, triggering a "StaleElementReferenceException"
        # which can be fixed, by selecting it (clicking) and find it again
        textarea = form_element.find_element(By.TAG_NAME, "textarea")
        textarea.click()

        # Find textarea again
        textarea = form_element.find_element(By.TAG_NAME, "textarea")
        write(textarea, text)  # Write comment

        # Submit the form
        textarea.send_keys(Keys.RETURN)

    @check_authorization
    def can_comment(self) -> bool:
        """
        Checks if you can comment on the post.

        Returns:
            bool: Whether you can comment.

        Raises:
            NotAuthenticated: Raises when the current account is not logged in.
        """
        self._driver.implicitly_wait(2)

        # Check for form elements
        found_elements = self._driver.find_elements(By.TAG_NAME, "form")

        self._driver.implicitly_wait(IMPLICIT_WAIT)
        return bool(found_elements)

    @check_authorization
    def get_date_posted(self) -> datetime:
        """
        Gets the date the the post was published.

        Returns:
            datetime: Publish date.
        """
        time_element = self._driver.find_element(By.CSS_SELECTOR, "time.x1p4m5qa")
        time_str = time_element.get_attribute("datetime")
        publish_date = parse_instagram_date(time_str)

        return publish_date
