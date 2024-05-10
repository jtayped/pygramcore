from datetime import datetime


def parse_instagram_date(time: str):
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
