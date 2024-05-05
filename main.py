from auth import Account
from elements.User import User

Account.login("jtayped@gmail.com", "tayped")

user = User("jtayped")
user.follow()