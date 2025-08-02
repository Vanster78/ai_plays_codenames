from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .game import CodenamesGame
from .websocket import ConnectionManager

app = FastAPI()

# Mount static files (for CSS)
app.mount("/static", StaticFiles(directory="ai_plays_codenames/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="ai_plays_codenames/templates")

# Initialize connection manager and a dummy game
manager = ConnectionManager()
# In a real app, you would manage multiple game instances
GAME_ID = "test_game"
game = CodenamesGame()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main game page."""
    game_state = game.get_state()
    return templates.TemplateResponse(
        "index.html", {"request": request, "game_state": game_state, "game_id": GAME_ID}
    )

@app.post("/move/{game_id}", response_class=HTMLResponse)
async def make_move(request: Request, game_id: str):
    """Handle a game action and broadcast the update."""
    game.reveal_random_card() # Simulate a move
    game_state = game.get_state()

    # Render the updated game board partial
    updated_board = templates.TemplateResponse(
        "partials/game_board.html", {"request": request, "game_state": game_state}
    ).body.decode()

    # Broadcast the HTML update to all clients
    await manager.broadcast(updated_board, game_id)
    return updated_board # Also return for the client that initiated the action

@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    """Handle WebSocket connections."""
    await manager.connect(websocket, game_id)
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)