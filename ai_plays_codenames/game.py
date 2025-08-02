import random

class CodenamesGame:
    """A simple dummy game state manager with team/player setup."""
    def __init__(self):
        words = ["Apple", "Car", "River", "Star", "Box", "Key", "Blue", "Dog", "Tree"]
        self.board = [{"word": word, "revealed": False} for word in words]
        self.teams = []
        self.teams_configured = False

    def setup_teams(self, teams):
        """Configure teams and players for the game."""
        self.teams = teams
        # Track color type for each team (red/blue)
        self.team_colors = [t.get("color", "red" if i == 0 else "blue") for i, t in enumerate(teams)]
        self.teams_configured = True if all(t["name"] and t["players"] for t in teams) else False

    def get_state(self):
        """Returns the current state of the board and teams."""
        return {
            "board": self.board,
            "teams": self.teams,
            "teams_configured": self.teams_configured,
        }

    def reveal_random_card(self):
        """Simulates a game move by revealing a random unrevealed card."""
        unrevealed_cards = [card for card in self.board if not card['revealed']]
        if unrevealed_cards:
            random.choice(unrevealed_cards)['revealed'] = True