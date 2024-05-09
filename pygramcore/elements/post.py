from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime

from pygram import Navigator, check_authorization
from exceptions.post import *
from utils import *
from constants import *


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
        """
        Gets the list of users the post was liked by.

        Args:
            limit (int): Maximum number of users. Defaults to 25 and can't be above 100.

        Returns:
            list[User]: List of Users.

        Raises:
            TooManyUsers: Raises when the limit is above 100.
        """
        from elements import User

        if limit > 100:
            raise TooManyUsers()

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
        image_urls = []
        while True:
            image_list_elements = self._driver.find_element(
                By.XPATH,
                '//div[@class="x6s0dn4 x1dqoszc xu3j5b3 xm81vs4 x78zum5 x1iyjqo2 x1tjbqro"]',
            )

            images = image_list_elements.find_elements(By.TAG_NAME, "img")

            new_image_urls = []
            for image in images:
                url = image.get_attribute("src")
                if url not in image_urls:
                    new_image_urls.append(url)

            image_urls.extend(new_image_urls)

            # Finding 1 image or less means that either there are no more posts in the list
            # or the post is of a single image (not a carousel)
            if len(new_image_urls) <= 1:
                break

            # An image loads on each side of the current index of a post, so to get the
            # next two posts, it shall double click the next button
            next_btn = self._driver.find_element(
                By.XPATH, '//button[@aria-label="Next"][@class=" _afxw _al46 _al47"]'
            )
            next_btn.click()

            # On the last image the next button will dissapear, so if it tries to click it
            # it will trigger the StaleElementReferenceException.
            try:
                next_btn.click()
            except StaleElementReferenceException:
                continue

        return image_urls

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
