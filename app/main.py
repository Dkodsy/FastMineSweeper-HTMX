from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.services.minesweeper import generate_content, generate_game_code, ActiveGame

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

active_game = ActiveGame()
connected_clients = []


# TODO подключение к одной и той же игре (на данный момент эта часть не работает)
@app.websocket("/ws/connected")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    connected_clients.append({"websocket": websocket})
    try:
        while True:
            data = await websocket.receive_json()
            for client in connected_clients:
                content = await generate_content(connection=websocket, data=data)
                await client["websocket"].send_text(content)
    except Exception as e:
        print(e)
        # TODO Фикс бага
        # "cannot call recv while another coroutine is already waiting for the next message"
        connected_clients.remove({"websocket": websocket})


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request) -> HTMLResponse:
    redirect_url = request.headers.get("redirect_url")
    if redirect_url:
        response = HTMLResponse()
        response.headers["HX-Redirect"] = redirect_url
        return response
    return templates.TemplateResponse("minesweeper_general.html", {"request": request})


@app.get("/create_game", response_class=HTMLResponse)
async def create_game(request: Request) -> HTMLResponse:
    # На данный момент /create_game содержит в себе логику подключения и
    # TODO создания игры
    random_number = await generate_game_code()
    active_game.game_code = random_number
    return templates.TemplateResponse(
        "create_game.html", {"request": request, "game_code": random_number}
    )
