from datetime import datetime
import time, random

def parse_instagram_date(time: str):
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")

def write(input, text, speed = 3):
    """
    Types some text letter by letter at random intervals in an input field. This is done so the interaction feels more "human-like".

    Args:
        input (WebElement): The input to write in.
        text (str): Text being written.
        speed (int): Divides the random float (from 0 to 1). The higher the number the faster it writes.
    """
    for letter in text:
        input.send_keys(letter)
        time.sleep(random.random() / speed)
