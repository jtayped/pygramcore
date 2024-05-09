class NotAuthenticated(Exception):
    def __init__(self):
        super().__init__("This is an authenticated action, please login beforehand.")
