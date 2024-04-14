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
        # self.connections: Dict[uuid.UUID, WebSocket] = {}

    # def add_user(self, user_id: uuid.UUID, websocket: WebSocket):
    #     """Add a user websocket, keyed by corresponding user ID.
    #
    #     Raises:
    #         ValueError: If the `user_id` already exists within the room.
    #     """
    #     if user_id in self.connections:
    #         raise ValueError(f"User {user_id} is already in the room")
    #     logger.info("Adding user %s to room", user_id)
    #     self.connections[user_id] = websocket
