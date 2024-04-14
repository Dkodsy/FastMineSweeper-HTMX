from fastapi import FastAPI, WebSocket, Request, Form
from fastapi.websockets import WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.game import Game
from app.services.connections import ConnectionManager

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

connection_manager = ConnectionManager()


@app.websocket("/game/{game_id}")
async def game_endpoint(websocket: WebSocket, game_id: str) -> None:
    await connection_manager.connect(websocket, game_id)
    try:
        while True:
            data = await websocket.receive_json()
            await connection_manager.broadcast(data, game_id)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/create_game", response_class=HTMLResponse)
async def get_create_game(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("create_game.html", {"request": request})


@app.post("/create_game", response_class=HTMLResponse)
async def create_game(request: Request,
                      player_count: int = Form(...),
                      board_size: str = Form(...),
                      time_limit: int = Form(...)
                      ):
    new_game = Game()
    response = HTMLResponse()
    response.headers["HX-Redirect"] = f'/game/{new_game.game_id}'
    return response


@app.get("/game/{game_id}", response_class=HTMLResponse)
async def join_game(request: Request, game_id: str) -> HTMLResponse:
    return templates.TemplateResponse("game.html", {"request": request, 'game_id': game_id})
