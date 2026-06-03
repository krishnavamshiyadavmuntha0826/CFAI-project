"""
player.py - Player types: Human and AI

HumanPlayer: prompts the user for input
AIPlayer: delegates move selection to an Agent
"""

from game import Game
from agent import Agent


class Player:
    """Base class for a game player."""

    def __init__(self, symbol: str):
        self.symbol = symbol

    def get_move(self, game: Game) -> int:
        raise NotImplementedError

    def __str__(self):
        return f"Player({self.symbol})"


class HumanPlayer(Player):
    """Gets move input from the human user."""

    def get_move(self, game: Game) -> int:
        legal = game.get_legal_moves()
        print(f"Legal moves: {legal}")
        while True:
            try:
                move = int(input("Enter your move (0-8): ").strip())
                if move in legal:
                    return move
                else:
                    print(f"Invalid! Choose from {legal}.")
            except ValueError:
                print("Please enter a valid number.")

    def __str__(self):
        return f"Human({self.symbol})"


class AIPlayer(Player):
    """Selects moves using an AI agent."""

    def __init__(self, symbol: str, agent: Agent):
        super().__init__(symbol)
        self.agent = agent

    def get_move(self, game: Game) -> int:
        print("AI is thinking...")
        move = self.agent.choose_move(game)
        print(f"AI chose: {move}")
        return move

    def __str__(self):
        return f"AI({self.symbol})"
