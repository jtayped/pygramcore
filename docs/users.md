# Users

`pygramcore` has a class that represents an Instagram account, which can be used by providing the username of the user.

```python
from pygramcore import User
user = User("username")
```

Example:

```python
# Please refer to getting-started.md guide for authentication.
if not user.is_following():
	user.follow()

total_followers = user.get_followers()
if followers > 100:
	user.send_dm("Hi! How is it going?")
```

## .is_private()

Checks if the user has a private account.

Returns:

- `bool`: Whether the account is private.

Raises:

- `NotAuthenticated`: Raises when the current account is not logged in.

## .follow()

Follows the user with the current account logged in.

Raises:

- `UserAlreadyFollowed`: Raises when the user is already followed. Use `.is_followed()` to check if followed.
- `NotAuthenticated`: Raises when the current account is not logged in.

## .unfollow()

Unfollows the user with the current account logged in.

Raises:

- `UserNotFollowed`: Raises when the user is not followed. Use `.is_followed()` to check if followed.
- `NotAuthenticated`: Raises when the current account is not logged in.

## .is_following()

Check whether the account logged in follows the user.

Returns:

- `bool`: whether the account logged in follows the user.

Raises:

- `NotAuthenticated`: Raises when the current account is not logged in.

## .add_close_friend()

Adds the user to the current account's close friends.

Raises:

- `UserCloseFriend`: Raises when the user is already a close friend.
- `NotAuthenticated`: Raises when the current account is not logged in.

## .remove_close_friend()

Removes the user from the current account's close friends.

Raises:

- `UserNotCloseFriend`: Raises when the user is not close friends already.
- `NotAuthenticated`: Raises when the current account is not logged in.

## .is_close_friend()

Checks if the user is a close friend.

Returns:

- `bool`: Whether the user is a close friend

Raises:

- `NotAuthenticated`: Raises when the current account is not logged in.

## .mute(\*modes)

Mutes the user's posts and/or stories. It is important to note that this function only enables the option, and can't disable it.

Args:

- `modes` ("posts" and/or "stories"): Modes to mute, which can be posts and/or stories.

Example:

```python
user = User("username")

# Mute the user's stories and posts
user.mute("stories", "posts")
```

Raises:

- `ValueError`: if a mode in the arguments does not exist.
- `NotAuthenticated`: Raises when the current account is not logged in.

## .get_total_posts()

Get the user's total amount of posts.

Returns:

- `int`: total posts

## .get_followers()

Get the user's total amount of followers

Returns:

- `int`: total followers

## .get_following()

Get the amount of people the user follows.

Returns:

- `int`: total following

## .send_dm(message)

Send a DM (direct message) to the user.

Args:
`message` (str): Message to send the user.

## .get_posts(reels=True, limit=25)

Get a list of posts from the user's account.

Args:

- `reels` (bool): Whether to include reels or not. Defaults to True.
- `limit` (int): Limits the amount of posts to retrieve. Defaults to 25 and can't be above 100.

Returns:

- `list[Post]`: List of post objects
- Usage:

```python
# Fetch username's posts
user = User("username")
posts = user.get_posts()

# Like his first three posts
for post in posts[:3]:
	post.like()
```
