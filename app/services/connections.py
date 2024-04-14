from typing import Annotated
from fastapi import WebSocket, Cookie, status, WebSocketException
from app.game import generate_content, Game


class ConnectionManager:
    def __init__(self):
        self.active_connections: [WebSocket] = []
        self.active_game_connections: dict[Game: [WebSocket]] = {}

    async def get_cookie(self, token: Annotated[str | None, Cookie()] = None):
        if token is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        return token

    async def connect(self, websocket: WebSocket, game_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        game_connections = self.active_game_connections.setdefault(game_id, [])
        if websocket not in game_connections:
            game_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        content = await generate_content(message)
        await websocket.send_text(content)

    async def broadcast(self, message: dict, game_id: str):
        content = await generate_content(message, game_id)
        for_users = self.active_game_connections.get(game_id, [])
        for connection in for_users:
            await connection.send_text(content)
