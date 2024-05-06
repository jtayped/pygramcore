<h1 align="center">
  <br>
  <img src="/images/icon.png" alt="PyGramCore" width="200">
  <br>
  📷 PyGramCore
  <br>
</h1>

<h4 align="center">An easy-to-use Instagram SDK using <a href="https://www.selenium.dev/" target="_blank">Selenium</a>.</h4>

<p align="center">
  <a href="https://pypi.org/project/PyGramCore/">
    <img src="https://img.shields.io/pypi/v/pygramcore?style=for-the-badge">
  </a>
  <a href="/LICENSE">
      <img src="https://img.shields.io/github/license/jtayped/pygramcore?style=for-the-badge" alt="License">
  </a>
    <a href="/issues">
      <img src="https://img.shields.io/github/issues/jtayped/pygramcore?style=for-the-badge" alt="License">
  </a>
  <a href="https://www.linkedin.com/in/jtayped/">
      <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#related">Related</a>
</p>

<div id="key-features"></div>

## 🔑 Key Features

- **Modular Elements**: Easily use and customize modular elements such as Posts, Comments, and Users.

  - **Users**: Follow, download posts, direct message, and more.

  - **Stories**: Like, download, reply and more.

  - **Posts**: Like, comment, save, download, and more.

  - **Comments**: Like, reply, and engage.

<div id="how-to-use"></div>

## ❔ How To Use

First of all, install the package using:

```bash
pip install pygramcore
```

To take authenticated actions, initialize your Instagram account with your email/password and login:

```python
from pygramcore.auth import Account
import pickle

account = Account("example@example.com", "yourpassword")
cookies = account.login() # might require interaction due to CAPTCHAs

# Your implementation to save cookies...
with open("path/to/cookies.pkl", 'wb') as file:
  pickle.dump(cookies, file)
```

To initialize an account from cookies:
```python
import pickle

# Your implementation to read cookies...
with open("path/to/cookies.pkl", 'rb') as file:
  cookies = pickle.load(file)

# Initialize the account with cookies
account = Account(cookies)
```

This will allow you to post images, comment on other peoples posts, send DMs, etc...

```python
# Post an image with an optional caption
account.post("path/to/image.png", "Your very interesting caption")
```

To search for a user simply:

```python
from pygramcore.elements.User import User

user = User("jtayped_")
```

Here is an example of the usage of a user:

```python
# Get a list of Post() objects
posts = user.get_posts(limit=50)

# Like the first 10 posts in the user's feed
for post in posts[:10]:
  post.like()

# Send a direct message to the user
user.send_dm("What's up?")
```

Please refer to the docs for more.

<div id="related"></div>

## 🙋‍♂️ You may also like...

- [TikTok Manager](https://github.com/jtayped/tiktok-manager) - A script that manages MULTIPLE TikTok accounts by schedueling automatically generated videos from pre-selected YouTube channels to TikTok in advance.
- [My Portfolio](https://joeltaylor.business) - Check out my front-end and SEO skills on my Portfolio!
