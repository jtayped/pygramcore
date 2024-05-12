class CannotFindComment(Exception):
    def __init__(self):
        super().__init__("Couldn't find the comment.")


class CommentLiked(Exception):
    def __init__(self):
        super().__init__("This comment has already been liked.")


class CommentNotLiked(Exception):
    def __init__(self):
        super().__init__("This comment has not been liked.")
