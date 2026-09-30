"""Flat Monte Carlo against MCTS on a back-rank trap (Figure 3 of part 1).

White to move. Qxd7 wins a free knight, but the queen is the only piece guarding
e1, so Black answers Re1 and it is mate. Both searches use the same rollout: six
random moves, then count the material.

    pip install chess
    python3 chess_trap.py       # about two seconds
"""
import math
import random
import chess
from mcts import uct_search, best_move

FEN = "4r1k1/3n1ppp/8/8/8/8/5PPP/3Q2K1 w - - 0 1"
VALUE = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}


class Chess:
    def __init__(self, board):
        self.board = board

    def copy(self):
        return Chess(self.board.copy())

    def legal_moves(self):
        return list(self.board.legal_moves)

    def play(self, move):
        self.board.push(move)

    def is_over(self):
        return self.board.is_game_over()

    def first_to_move(self):
        return self.board.turn == chess.WHITE


def white_score(board):
    """1 if White has won, 0 if Black has, otherwise a squashed material count."""
    if board.is_checkmate():
        return 0.0 if board.turn == chess.WHITE else 1.0
    if board.is_game_over():
        return 0.5
    material = sum(VALUE[p.piece_type] * (1 if p.color == chess.WHITE else -1)
                   for p in board.piece_map().values())
    return 0.5 + 0.5 * math.tanh(material / 5)


def rollout(state, rng, plies=6):
    board = state.board.copy(stack=False)
    for _ in range(plies):
        if board.is_game_over():
            break
        board.push(rng.choice(list(board.legal_moves)))
    return white_score(board)


def flat_monte_carlo(fen, games=400, seed=1):
    """Random games after each root move, no tree."""
    rng, board, scores = random.Random(seed), chess.Board(fen), {}
    for move in board.legal_moves:
        after = board.copy()
        after.push(move)
        scores[board.san(move)] = sum(rollout(Chess(after), rng) for _ in range(games)) / games
    return scores


if __name__ == "__main__":
    board = chess.Board(FEN)
    flat = flat_monte_carlo(FEN)
    print("flat Monte Carlo:", ", ".join(f"{m} {v:.3f}" for m, v in sorted(flat.items(), key=lambda kv: -kv[1])[:5]))
    root = uct_search(Chess(board), rollout, 5000, c=0.7, seed=0)
    print("MCTS visits:     ", ", ".join(f"{board.san(ch.move)} {ch.n}" for ch in sorted(root.children, key=lambda ch: -ch.n)[:6]))
    trap = next(ch for ch in root.children if board.san(ch.move) == "Qxd7")
    print("Qxd7 visits:     ", trap.n)
    print("play:", board.san(best_move(root)))
