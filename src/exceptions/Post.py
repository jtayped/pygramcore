class PostLiked(Exception):
    def __init__(self):
        super().__init__("This post has already been liked.")


class PostNotLiked(Exception):
    def __init__(self):
        super().__init__("This post has not been liked.")


class CannotComment(Exception):

    def __init__(self):
        super().__init__("This post can't be commented on.")


class TooManyUsers(Exception):

    def __init__(self):
        super().__init__("There aren't enough users in the list.")
