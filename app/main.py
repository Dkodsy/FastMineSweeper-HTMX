from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

connected_clients = []


@app.websocket("/ws/connected")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    connected_clients.append({"websocket": websocket})
    try:
        while True:
            data = await websocket.receive_json()
            content = """
                    <div hx-swap-oob="beforeend:#content">
                    <p>{time}: {message}</p>
                    </div>
                """
            for client in connected_clients:
                content = content.format(
                    time=data["chat_message"], message=data["chat_message"]
                )

                await client["websocket"].send_text(content)
    except Exception as e:
        print(e)
        connected_clients.remove({"websocket": websocket})


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("minesweeper_general.html", {"request": request})
