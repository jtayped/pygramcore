from dataclasses import dataclass
from typing import ClassVar
from selenium.webdriver.common.by import By
from selenium import webdriver

from exceptions.post import *
from constants import *
from pygram import Navigator, check_authorization


@dataclass
class Post(metaclass=Navigator):
    id: str

    # To identify state of the button
    liked_selector: ClassVar[str] = "svg[aria-label='Like'][width='24']"
    unlike_selector: ClassVar[str] = "svg[aria-label='Unlike'][width='24']"

    # To toggle the button
    like_btn: ClassVar[str] = (
        "#mount_0_0_cz > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y > section > main > div > div.x6s0dn4.x78zum5.xdt5ytf.xdj266r.xkrivgy.xat24cr.x1gryazu.x1n2onr6.xh8yej3 > div > div.x4h1yfo > div > div.x1xp8e9x.x13fuv20.x178xt8z.x9f619.x1yrsyyn.x1pi30zi.x10b6aqq.x1swvt13.xh8yej3 > section.x6s0dn4.xrvj5dj.x1o61qjw > div.x78zum5 > span.xp7jhwk"
    )

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

        if self._driver.find_elements(By.CSS_SELECTOR, self.liked_selector):
            self._driver.implicitly_wait(10)
            return False
        elif self._driver.find_elements(By.CSS_SELECTOR, self.unlike_selector):
            self._driver.implicitly_wait(10)
            return True

    def get_likes(self) -> int:
        pass

    def get_images(self) -> list[str]:
        pass

    def get_comments(self, limit=10) -> list[object]:
        pass

    def comment(self) -> object:
        pass
