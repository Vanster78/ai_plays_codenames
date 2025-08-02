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

# Store setup state in memory for now
setup_state = {"teams": [
    {"name": "", "players": []},
    {"name": "", "players": []}
]}


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main game page or setup screen."""
    # If teams are not configured, show setup
    game_state = game.get_state()
    if not getattr(game_state, 'teams_configured', False):
        # Pass a dummy game_state with teams_configured = False
        return templates.TemplateResponse(
            "index.html", {"request": request, "game_state": {"teams_configured": False}, "game_id": GAME_ID}
        )
    return templates.TemplateResponse(
        "index.html", {"request": request, "game_state": game_state, "game_id": GAME_ID}
    )
from fastapi import Form

@app.post("/setup", response_class=HTMLResponse)
async def setup_game(request: Request):
    """Handle setup form submission and initialize game."""
    form = await request.form()
    # Parse teams and players
    teams = []
    for team_idx in [0, 1]:
        team_name = form.get(f"team_name_{team_idx}", "Red" if team_idx == 0 else "Blue")
        team_color = form.get(f"team_color_{team_idx}", "red" if team_idx == 0 else "blue")
        players = []
        i = 0
        while True:
            ptype = form.get(f"player_type_{team_idx}_{i}")
            if ptype is None:
                break
            pname = form.get(f"player_name_{team_idx}_{i}", "")
            if not pname:
                pname = ptype if ptype != "Human" else "Human"
            players.append({"type": ptype, "name": pname})
            i += 1
        teams.append({"name": team_name, "color": team_color, "players": players})
    setup_state["teams"] = teams
    # Configure the game instance
    game.setup_teams(teams)
    # Render the game board
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