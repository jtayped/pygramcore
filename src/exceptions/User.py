class UserAlreadyFollowed(Exception):
    def __init__(self, username: str) -> None:
        super().__init__(f"You already follow {username}.")


class UserNotFollowed(Exception):
    def __init__(self, username: str) -> None:
        super().__init__(f"You don't follow {username} yet.")


class UserCloseFriend(Exception):
    def __init__(self, username: str) -> None:
        super().__init__(f"You are already close friends with {username}.")


class UserNotCloseFriend(Exception):
    def __init__(self, username: str) -> None:
        super().__init__(f"You haven't added {username} to your close friends yet.")
