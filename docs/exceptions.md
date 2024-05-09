## Exceptions

All exceptions are stored in `pygramcore.exceptions`. Here is an example of how to handle exceptions:

```python
from pygramcore.exceptions.user import UserNotFollowed

user = User("username")

try:
	user.unfollow()
except UserNotFollowed as e:
	print(e)
```
