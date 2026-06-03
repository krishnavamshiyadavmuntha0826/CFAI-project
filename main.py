"""
Board Game Playing Agent
========================
A modular board game framework featuring a Minimax AI agent with Alpha-Beta pruning.
Currently supports Tic-Tac-Toe. Easily extensible to other games.
"""

from game import TicTacToe
from agent import MinimaxAgent
from player import HumanPlayer, AIPlayer


def main():
    print("=" * 40)
    print("   BOARD GAME PLAYING AGENT")
    print("=" * 40)
    print("\nGame: Tic-Tac-Toe")
    print("\nSelect mode:")
    print("  1. Human vs AI")
    print("  2. AI vs AI")
    print("  3. Human vs Human")

    choice = input("\nEnter choice (1/2/3): ").strip()

    game = TicTacToe()

    if choice == "1":
        player_x = HumanPlayer("X")
        player_o = AIPlayer("O", MinimaxAgent(player_symbol="O", opponent_symbol="X"))
    elif choice == "2":
        player_x = AIPlayer("X", MinimaxAgent(player_symbol="X", opponent_symbol="O"))
        player_o = AIPlayer("O", MinimaxAgent(player_symbol="O", opponent_symbol="X"))
    else:
        player_x = HumanPlayer("X")
        player_o = HumanPlayer("O")

    players = {"X": player_x, "O": player_o}
    current = "X"

    print("\n")
    game.display()

    while not game.is_terminal():
        print(f"\n--- {players[current]}'s turn ({current}) ---")
        move = players[current].get_move(game)

        if move not in game.get_legal_moves():
            print("Invalid move! Try again.")
            continue

        game.make_move(move, current)
        game.display()
        current = "O" if current == "X" else "X"

    winner = game.get_winner()
    print("\n" + "=" * 40)
    if winner:
        print(f"🎉 Player '{winner}' WINS!")
    else:
        print("🤝 It's a DRAW!")
    print("=" * 40)


if __name__ == "__main__":
    main()
