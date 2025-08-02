import random

class CodenamesGame:
    """A simple dummy game state manager."""
    def __init__(self):
        words = ["Apple", "Car", "River", "Star", "Box", "Key", "Blue", "Dog", "Tree"]
        self.board = [{"word": word, "revealed": False} for word in words]

    def get_state(self):
        """Returns the current state of the board."""
        return self.board

    def reveal_random_card(self):
        """Simulates a game move by revealing a random unrevealed card."""
        unrevealed_cards = [card for card in self.board if not card['revealed']]
        if unrevealed_cards:
            random.choice(unrevealed_cards)['revealed'] = True