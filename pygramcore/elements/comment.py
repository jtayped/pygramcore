from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from dataclasses import dataclass
from datetime import datetime

from ..exceptions.comment import *
from ..exceptions.post import CannotComment
from ..utils import *
from ..pygram import *


@dataclass
class Comment:
    from .user import User
    from .post import Post

    author: User
    post: Post
    date: datetime
    text: str = None
    likes: int = None

    @property
    def url(self):
        return self.post.url

    @property
    @check_authorization
    def likes(self):
        comment_element = self.__find_comment()
        comment_functions_element = comment_element.find_element(
            By.XPATH,
            '//div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1xmf6yo x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1"]',
        )
        likes_element, _ = comment_functions_element.find_elements(
            By.XPATH,
            '//span[@class="x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft"]',
        )

        # Convert the likes element to an integer (E.g. "11,560 likes" to 11560)
        likes = int(likes_element.text.removesuffix(" likes").replace(",", ""))
        return likes

    @check_authorization
    def like(self):
        comment_element = self.__find_comment()

        if self.is_liked():
            raise CommentLiked

        like_btn = comment_element.find_element(
            By.CSS_SELECTOR, 'svg[aria-label="Like"]'
        )
        like_btn.click()

    @check_authorization
    def unlike(self):
        comment_element = self.__find_comment()

        if self.is_liked():
            raise CommentNotLiked

        like_btn = comment_element.find_element(
            By.CSS_SELECTOR, 'svg[aria-label="Unlike"]'
        )
        like_btn.click()

    @check_authorization
    def is_liked(self):
        comment_element = self.__find_comment()

        like_btn = comment_element.find_element(
            By.XPATH, '//span[@class="x1ykxiw6 x4hg4is x3oybdh"]//svg'
        )
        liked_value = like_btn.get_attribute("aria-label")

        return liked_value == "Unlike"

    @check_authorization
    def reply(self, message: str):
        # You can't reply to comments in posts where you can't comment.
        if not self.post.can_comment():
            raise CannotComment

        comment_element = self.__find_comment()
        # TODO

    def __find_comment(self, max_depth=200) -> WebElement:
        """
        Navigates to the parent post and scrolls till the comment has been found or the maximum depth has been exceded.

        Args:
            max_depth (int) = Limits the number of comments to search through.

        Returns:
            WebElement: The div associated to the comment.
        """
        # Navigate to the post that parents the comment
        navigate(self._driver, self.post.url)

        # TODO: implement the logic
        return

        # If not found raise an error
        raise CannotFindComment
