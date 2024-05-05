from dataclasses import dataclass

from utils.auth import check_auth

@dataclass
class User:
    """
    Represents an Instagram user.

    Args:
        name (str): Username of the user.
    """
    name: str
    
    @check_auth
    def follow(self):
        print("authed")

    def get_posts(self):
        pass