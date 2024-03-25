from typing import List, Set
from fastapi import WebSocket
import random
import string


# TODO Разделить логику по директориям генерации html ответов для фронта, логику игры, сервис создания/подключения


class ActiveGame:
    def __init__(self):
        self.connections: Set[WebSocket] = set()
        self.game_code: str = ""


async def generate_content(connection: WebSocket, data: dict) -> str:
    """
    :param connection: WebSocket connection #todo-delete возможно мусор
    :param data: Dictionary with receive message from user
    :return: Content for display on web page
    """
    content = """
        <div hx-swap-oob="beforeend:#content">
        <p>{time}: {message}</p>
        </div>
    """.format(time=data["chat_message"], message=data["chat_message"])
    return content


async def generate_game_code() -> str:
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = "".join(random.sample(letters_and_digits, 6))
    return rand_string
