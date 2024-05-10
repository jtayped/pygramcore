# Posts

`pygramcore` has a class that represents posts on Instagram, which can be referenced from their IDs. These IDs can be found in the post URL, for example, this post's ID `https://www.instagram.com/p/CmUv48DLvxd` is `CmUv48DLvxd`. A post can be initialized like so:

```python
from pygramcore import Post
post = Post("CmUv48DLvxd")
```

Example:

```python
# Like the post if not liked yet
if not post.is_liked():
	post.like()

# Comment on the post
if post.can_comment():
	post.comment("Amazing post!")

# Follow 5 people who liked the post
users = post.get_liked_by(limit=5)
for user in users:
	if not user.is_followed()
		user.follow()
```

## .like()

Likes the post.

Raises:

- `PostLiked`: Raises when the post is already liked.
- `NotAuthenticated`: Raises when the current account is not logged in.

## .unlike()

Unlikes the post.

Raises:

- `PostNotLiked`: Raises when the post is not liked already.
- `NotAuthenticated`: Raises when the current account is not logged in.

## .is_liked()

Checks whether the post is liked.

Returns:

- `bool`: whether the post is liked.

Raises:

- `NotAuthenticated`: Raises when the current account is not logged in.

## . get_total_likes()

Returns the total amount of likes.

Returns:

- `int`: Number of likes

Raises:

- `NotAuthenticated`: Raises when the current account is not logged in.

## .get_liked_by(limit=25)

Gets the list of users the post was liked by.

Args:

- `limit` (int): Maximum number of users. Defaults to 25 and can't be above 100.

Returns:

- `list[User]`: List of Users.

Raises:

- `TooManyUsers`: Raises when the limit is above 100.

## .get_images()

Gets list of images from the post.

Returns:

- `list[str]`: List of image URLs

Raises:

- `NotAuthenticated`: Raises when the current account is not logged in.

## .comment(text)

Comments on the post.

Args:

- `text` (str): The comment.

Raises:

- `CannotComment`: Whether you can comment.
- `NotAuthenticated`: Raises when the current account is not logged in.

## .can_comment()

Checks if you can comment on the post.

Returns:

- `bool`: Whether you can comment.

Raises:

- `NotAuthenticated`: Raises when the current account is not logged in.

## .get_date_posted()

Gets the date the the post was published.

Returns:

- `datetime`: Publish date.

## .get_author()

Finds the user who created the post.

Returns:

- `User`: Author's user object.

Raises:

- `NotAuthenticated`: Raises when the current account is not logged in.
