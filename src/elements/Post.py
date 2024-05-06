from dataclasses import dataclass
from elements.Comment import Comment

@dataclass
class Post:
    id: str

    def like(self) -> None:
        pass

    def get_likes(self) -> int:
        pass

    def get_images(self) -> list[str]:
        pass

    def get_comments(self, limit=10) -> list[Comment]:
        pass

    def comment(self) -> Comment:
        pass
