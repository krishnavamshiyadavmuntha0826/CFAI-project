"""
game.py - Game logic for Tic-Tac-Toe
Implements the base Game interface for easy extension to other board games.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple


class Game(ABC):
    """Abstract base class for board games."""

    @abstractmethod
    def get_legal_moves(self) -> List:
        pass

    @abstractmethod
    def make_move(self, move, player: str) -> None:
        pass

    @abstractmethod
    def undo_move(self, move) -> None:
        pass

    @abstractmethod
    def is_terminal(self) -> bool:
        pass

    @abstractmethod
    def get_winner(self) -> Optional[str]:
        pass

    @abstractmethod
    def evaluate(self, player: str, opponent: str) -> int:
        pass

    @abstractmethod
    def display(self) -> None:
        pass

    @abstractmethod
    def clone(self) -> "Game":
        pass


class TicTacToe(Game):
    """
    Standard 3x3 Tic-Tac-Toe game.

    Board positions:
        0 | 1 | 2
       -----------
        3 | 4 | 5
       -----------
        6 | 7 | 8
    """

    WIN_CONDITIONS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6),             # Diagonals
    ]

    def __init__(self):
        self.board = [None] * 9
        self._move_history = []

    def get_legal_moves(self) -> List[int]:
        return [i for i, cell in enumerate(self.board) if cell is None]

    def make_move(self, move: int, player: str) -> None:
        if self.board[move] is not None:
            raise ValueError(f"Cell {move} is already occupied.")
        self.board[move] = player
        self._move_history.append(move)

    def undo_move(self, move: int) -> None:
        self.board[move] = None
        if self._move_history and self._move_history[-1] == move:
            self._move_history.pop()

    def is_terminal(self) -> bool:
        return self.get_winner() is not None or len(self.get_legal_moves()) == 0

    def get_winner(self) -> Optional[str]:
        for a, b, c in self.WIN_CONDITIONS:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def evaluate(self, player: str, opponent: str) -> int:
        """Returns +10 if player wins, -10 if opponent wins, 0 for draw."""
        winner = self.get_winner()
        if winner == player:
            return 10
        elif winner == opponent:
            return -10
        return 0

    def display(self) -> None:
        symbols = {None: ".", "X": "X", "O": "O"}
        rows = []
        for row in range(3):
            cells = [symbols[self.board[row * 3 + col]] for col in range(3)]
            rows.append(" | ".join(cells))
        print("\n" + "\n---+---+---\n".join(rows) + "\n")

    def clone(self) -> "TicTacToe":
        new_game = TicTacToe()
        new_game.board = self.board.copy()
        new_game._move_history = self._move_history.copy()
        return new_game
