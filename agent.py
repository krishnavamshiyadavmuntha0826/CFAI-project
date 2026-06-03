"""
agent.py - AI Agent using Minimax with Alpha-Beta Pruning

The MinimaxAgent explores the game tree to find the optimal move,
using alpha-beta pruning to skip branches that can't affect the result.
"""

import math
from typing import Optional, Tuple
from game import Game


class Agent:
    """Base class for all game-playing agents."""

    def choose_move(self, game: Game) -> int:
        raise NotImplementedError


class MinimaxAgent(Agent):
    """
    Minimax Agent with Alpha-Beta Pruning.

    - Maximizes score for `player_symbol`
    - Minimizes score for `opponent_symbol`
    - Prunes branches using alpha-beta to improve efficiency
    """

    def __init__(self, player_symbol: str, opponent_symbol: str):
        self.player = player_symbol
        self.opponent = opponent_symbol

    def choose_move(self, game: Game) -> int:
        """Returns the best move index for the current game state."""
        best_score = -math.inf
        best_move = None

        for move in game.get_legal_moves():
            game.make_move(move, self.player)
            score = self._minimax(
                game, depth=0, is_maximizing=False,
                alpha=-math.inf, beta=math.inf
            )
            game.undo_move(move)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(
        self,
        game: Game,
        depth: int,
        is_maximizing: bool,
        alpha: float,
        beta: float
    ) -> int:
        """
        Recursive Minimax with Alpha-Beta pruning.

        Args:
            game: Current game state
            depth: Current depth in the tree
            is_maximizing: True if it's the maximizing player's turn
            alpha: Best score the maximizer can guarantee
            beta: Best score the minimizer can guarantee

        Returns:
            The evaluated score of the position
        """
        if game.is_terminal():
            score = game.evaluate(self.player, self.opponent)
            # Prefer faster wins / slower losses
            return score - depth if score > 0 else score + depth

        if is_maximizing:
            max_eval = -math.inf
            for move in game.get_legal_moves():
                game.make_move(move, self.player)
                eval_score = self._minimax(game, depth + 1, False, alpha, beta)
                game.undo_move(move)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = math.inf
            for move in game.get_legal_moves():
                game.make_move(move, self.opponent)
                eval_score = self._minimax(game, depth + 1, True, alpha, beta)
                game.undo_move(move)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval
