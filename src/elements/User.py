from dataclasses import dataclass

from utils.auth import check_auth
from elements.Post import Post


@dataclass
class User:
    """
    Represents an Instagram user.

    Args:
        name (str): Username of the user.
    """

    name: str

    def is_private(self) -> bool:
        pass

    def follow(self) -> None:
        pass

    def unfollow(self) -> None:
        pass

    def get_followers(self) -> int:
        pass

    def get_following(self) -> int:
        pass

    def send_dm(self, message: str) -> None:
        pass

    def get_posts(self, limit=10) -> list[Post]:
        pass
