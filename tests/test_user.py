from pygramcore.exceptions.user import *
from pygramcore import User, Account

import pytest


class TestUser:
    def setup_method(self):
        Account.load_cookies("cookies.pkl")

    def test_follow(self, user: User):
        was_following = user.is_following()

        # Test exceptions
        with pytest.raises(UserAlreadyFollowed):
            if not was_following:
                user.follow()

            user.follow()

        with pytest.raises(UserNotFollowed):
            if was_following:
                user.unfollow()

            user.unfollow()

        # Toggle follow options
        if was_following:
            user.unfollow()
            user.follow()
        else:
            user.follow()
            user.unfollow()

        # Reset follow state
        if was_following and not user.is_following():
            user.follow()
        elif not was_following and user.is_following():
            user.unfollow()
