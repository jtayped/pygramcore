class PostLiked(Exception):
    def __init__(self):
        super().__init__("This post has already been liked.")


class PostNotLiked(Exception):
    def __init__(self):
        super().__init__("This post has not been liked.")