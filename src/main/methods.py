from random import randint
from main.settings import VK_API


def send_message(text):
    VK_API.messages.send(
        user_id=443194153,
        message=text,
        random_id=randint(-2147483648, +2147483647),
    )
