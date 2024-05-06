from dataclasses import dataclass
from datetime import datetime

from utils.misc import parse_instagram_date


@dataclass
class Comment:
    author: str
    date_posted: str | datetime
    text: str

    def __post_init__(self):
        # Convert the strings to approrpriate objects if strings
        if isinstance(self.date_posted, str):
            self.date_posted = parse_instagram_date(self.date_posted)
        #if isinstance(self.author, str):
        #    self.author = User(self.author)

    def like(self) -> None:
        pass

    def get_likes(self) -> int:
        pass

    def get_comments(self) -> list["Comment"]:
        pass

    def reply(self) -> None:
        pass
