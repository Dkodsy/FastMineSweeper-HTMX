import random
import string


def generate_game_uuid() -> str:
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = "".join(random.sample(letters_and_digits, 6))
    return rand_string


async def generate_content(data: dict, game_id: str) -> str:
    """
    :param data: Dictionary with receive message from user
    :return: Content for display on web page
    """
    content = """
        <div hx-swap-oob="beforeend:#content">
        <p>{time}: {message}: {game_id}</p>
        </div>
    """.format(time=data["chat_message"], message=data["chat_message"], game_id=game_id)
    return content


class Game:
    """Game state, comprising connected users."""

    def __init__(self):
        self.game_id: str = generate_game_uuid()
