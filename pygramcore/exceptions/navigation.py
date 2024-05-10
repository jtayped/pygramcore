class PageNotFound(Exception):
    def __init__(self, url: str):
        super().__init__(f'"{url}"" Not found')
