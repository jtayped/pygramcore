from pygramcore import User, Post
import pytest

DEFAULT_USER = "champagnepapi"
DEFAULT_POST = "C5ZiDVruR2f"

@pytest.fixture
def user():
    return User(DEFAULT_USER)


@pytest.fixture
def post():
    return Post(DEFAULT_POST)
