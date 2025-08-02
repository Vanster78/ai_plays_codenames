# Copilot Instructions for ai_plays_codenames

## Project Overview
- This project implements AI agents playing the board game "Codenames" via a web interface.
- Main package: `ai_plays_codenames` (see `ai_plays_codenames/` directory).
- The `ai_codenames/` is a virtual environment directory that contains dependencies and should not be modified directly. It is used to isolate the project environment.

## Target Pipeline
- Configure players for each team (AI agents from a specific list or human players);
- Select cards from a predefined set, or generate them dynamically;
- Implement game rules and logic for Codenames;
- Implement AI strategies for guessing words based on clues;
- Provide a smooth web interface for users to observe the game;
- Add human player interaction capabilities, such as providing clues or making guesses.

## Requirements
- The project should be structured to allow easy addition of new game rules and AI strategies.
- The AI agents should be able to play the game autonomously, making decisions based on the game state.
- The web interface should provide a clear and interactive way for users to observe the game and interact with the AI agents.
- The system should support real-time updates to the game state, allowing users to see changes as they happen.

## Future Features
- Collect observations and actions from the AI agents to improve their performance over time with reinforcement learning.
- Use text-to-image models to generate visual representations of the cards.
- Use multimodal models to enable different input and output formats, such as voice replicas or visual cues.

## Architecture & Key Components
- `app.py`: Entry point for the FastAPI web application.
- `websocket.py`: Handles real-time communication for live game updates between clients and server.
- `static/` and `templates/`: Frontend assets (CSS, HTML, Jinja templates). `templates/partials/game_board.html` is a key UI component.

## Developer Workflows
- **Run the app:** Use `python run.py` or run `app.py` directly. (Check for Flask or similar usage.)
- **Install dependencies:** Use `pip install -e .` (editable mode) after ensuring `pyproject.toml` includes only `ai_plays_codenames` as the package.
- **Virtual environment:** Use the provided `ai_codenames/` venv (activate with `source ai_codenames/bin/activate`).
- **No explicit test suite** detected; add tests in `ai_plays_codenames/tests/` if needed.

## Project-Specific Patterns
- All backend logic is in `ai_plays_codenames/`.
- Websocket communication is separated into its own module (`websocket.py`).
- HTML templates are organized with partials for modularity.

## Integration & External Dependencies
- No external APIs or services are referenced in the top-level docs, but check `requirements.txt` for AI/ML libraries or web frameworks.
- All static and template files are referenced relative to the `ai_plays_codenames/` directory.

## Examples
- To update the UI, edit `templates/partials/game_board.html` and `static/style.css`.
- To add a new websocket event, update `websocket.py` and the relevant JS in `static/`.

## References
- See `README.md` for a high-level project description.
- See `pyproject.toml` for build/package configuration.

---
If any conventions or workflows are unclear, ask the user for clarification or examples from their recent work.
