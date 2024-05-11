from pygramcore.exceptions.user import *
from pygramcore import User, Account

import pytest


class TestUser:
    def setup_method(self):
        Account.load_cookies("cookies.pkl")

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
            user.unfollow()

        # Reset follow state (cleanup)
        if was_following:
            user.follow()
