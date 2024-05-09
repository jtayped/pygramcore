# Getting started

Using `pygramcore` does not require you to insert any account information. With this, you can retrieve publicly available data such as total followers, posts, and following.

## Authentication

To perform authenticated actions such as commenting and posting, you need to have a pre-existing Instagram account created with credentials (email/password). To log in, you can follow these simple steps:

```python
from pygramecore import Account

# Log in to the account using credentials
Account.login("youremail@email.com", "yourpassword123")
```

It is recommended to save a file containing the cookies associated with the session. This can be done by providing a file path:

```python
# Save cookies to a file
Account.save_cookies("path/to/cookies.pkl")
```

Later, you can load the cookies into the session to automatically authenticate the account:

```python
# Load cookies from a file
Account.load_cookies("path/to/cookies.pkl")
```
