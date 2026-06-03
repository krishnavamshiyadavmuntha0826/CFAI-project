"""
tests.py - Unit tests for Board Game Playing Agent
Run with: python tests.py
"""

import unittest
from game import TicTacToe
from agent import MinimaxAgent


class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        self.game = TicTacToe()

    def test_initial_board_is_empty(self):
        self.assertEqual(self.game.get_legal_moves(), list(range(9)))

    def test_make_and_undo_move(self):
        self.game.make_move(4, "X")
        self.assertEqual(self.game.board[4], "X")
        self.game.undo_move(4)
        self.assertIsNone(self.game.board[4])

    def test_winner_detection_row(self):
        for i in range(3):
            self.game.make_move(i, "X")
        self.assertEqual(self.game.get_winner(), "X")

    def test_winner_detection_diagonal(self):
        for i in [0, 4, 8]:
            self.game.make_move(i, "O")
        self.assertEqual(self.game.get_winner(), "O")

    def test_draw_detection(self):
        # X O X
        # X X O
        # O X O
        moves = [(0, "X"), (1, "O"), (2, "X"),
                 (3, "X"), (4, "X"), (5, "O"),
                 (6, "O"), (7, "X"), (8, "O")]
        for pos, p in moves:
            self.game.make_move(pos, p)
        self.assertIsNone(self.game.get_winner())
        self.assertTrue(self.game.is_terminal())

    def test_evaluate_win(self):
        for i in range(3):
            self.game.make_move(i, "X")
        self.assertEqual(self.game.evaluate("X", "O"), 10)
        self.assertEqual(self.game.evaluate("O", "X"), -10)

    def test_clone_independence(self):
        self.game.make_move(0, "X")
        clone = self.game.clone()
        clone.make_move(1, "O")
        self.assertIsNone(self.game.board[1])  # Original unchanged


class TestMinimaxAgent(unittest.TestCase):

    def setUp(self):
        self.agent = MinimaxAgent(player_symbol="O", opponent_symbol="X")

    def test_agent_blocks_winning_move(self):
        """AI should block X from winning at position 2."""
        game = TicTacToe()
        game.make_move(0, "X")
        game.make_move(1, "X")
        # X X _ -> AI (O) must play 2 to block
        move = self.agent.choose_move(game)
        self.assertEqual(move, 2)

    def test_agent_takes_winning_move(self):
        """AI should take position 8 to win."""
        game = TicTacToe()
        game.make_move(0, "O")
        game.make_move(4, "O")
        # O _ _
        # _ O _
        # _ _ _  -> AI should play 8 to win diagonally
        move = self.agent.choose_move(game)
        self.assertEqual(move, 8)

    def test_agent_returns_valid_move(self):
        """Agent always returns a legal move."""
        game = TicTacToe()
        for _ in range(3):
            move = self.agent.choose_move(game)
            self.assertIn(move, game.get_legal_moves())
            game.make_move(move, "O")
            if not game.is_terminal():
                remaining = game.get_legal_moves()
                game.make_move(remaining[0], "X")


if __name__ == "__main__":
    unittest.main(verbosity=2)
