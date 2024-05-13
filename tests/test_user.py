from pygramcore.exceptions.user import *
from pygramcore import User, Account
from dotenv import load_dotenv
import os

import pytest


class TestUser:
    @classmethod
    def setup_class(self):
        load_dotenv()

        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")

    def test_login(self):
        Account.login(self.email, self.password)

    def test_follow(self, user: User):
        was_following = user.is_following()

        # Toggle follow options
        if was_following:
            user.unfollow()
            user.follow()
        else:
            user.follow()
            user.unfollow()

        # Test exceptions
        with pytest.raises(UserAlreadyFollowed):
            if not was_following:
                user.follow()

            user.follow()

        with pytest.raises(UserNotFollowed):
            user.unfollow()

            # Unfollowing again should raise the error
            user.unfollow()

    def test_close_friends(self, user: User):
        # If the user is not followed, checking if the user is a close friend simply
        # returns false. By following the user, it requires the function to actually check.
        if not user.is_following():
            user.follow()

        is_close_friend = user.is_close_friend()

        # Toggle close friends
        if is_close_friend:
            user.remove_close_friend()
            user.add_close_friend()
        else:
            user.add_close_friend()
            user.remove_close_friend()

        # Test exceptions
        with pytest.raises(UserCloseFriend):
            if not is_close_friend:
                user.add_close_friend()

            user.add_close_friend()

        with pytest.raises(UserNotCloseFriend):
            user.remove_close_friend()

            # Removing from close friends again should raise the error
            user.remove_close_friend()

    def test_private_accounts(self, user: User, private_user: User):
        assert not user.is_private()  # expected: True
        assert private_user.is_private()  # expected: False

    def test_get_posts(self, user: User):
        # It should not be assumed that the user will not delete their posts.
        # This is why the max number of posts is anything below 5.
        total_posts = user.get_total_posts()
        n_posts = min(5, total_posts)

        posts = user.get_posts(limit=n_posts)
        assert len(posts) == n_posts
