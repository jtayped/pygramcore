from dataclasses import dataclass


@dataclass
class User:
    name: str

    def follow(self):
        pass

    def get_posts(self):
        pass