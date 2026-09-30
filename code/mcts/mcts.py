"""Plain Monte Carlo tree search (UCT) for two-player games.

A game state needs five methods:
    copy()           an independent copy
    legal_moves()    a list of the moves available
    play(move)       apply a move in place
    is_over()        True once the game has ended
    first_to_move()  True when the first player (Black in Go, White in chess) is to move

You also pass rollout(state, rng), which plays the game out from `state` and
returns the result for the first player: 1 for a win, 0 for a loss, or anything
in between. Used by go7x7.py and chess_trap.py, and explained in
https://cgnarendiran.github.io/blog/mcts-alphazero/
"""
import math
import random


class Node:
    def __init__(self, state, move=None, parent=None):
        self.move, self.parent, self.children = move, parent, []
        self.untried = state.legal_moves()            # moves not in the tree yet
        self.first_moved = not state.first_to_move()  # did the first player make `move`?
        self.n, self.w = 0, 0.0                       # visits, total result for that player


def uct_search(root_state, rollout, n_simulations, c=1.0, seed=0, on_step=None):
    rng = random.Random(seed)
    root = Node(root_state)
    for t in range(1, n_simulations + 1):
        node, state = root, root_state.copy()

        # 1. Select: walk down through fully expanded nodes by UCT score
        while not node.untried and node.children:
            log_n = math.log(node.n)
            node = max(node.children,
                       key=lambda ch: ch.w / ch.n + c * math.sqrt(log_n / ch.n))
            state.play(node.move)

        # 2. Expand: add one untried move to the tree
        if node.untried and not state.is_over():
            move = node.untried.pop(rng.randrange(len(node.untried)))
            state.play(move)
            child = Node(state, move, node)
            node.children.append(child)
            node = child

        # 3. Simulate: play the rest of the game out at random
        result = rollout(state, rng)

        # 4. Back up: every node on the path scores the result for its mover
        while node is not None:
            node.n += 1
            node.w += result if node.first_moved else 1 - result
            node = node.parent

        if on_step:
            on_step(t, root)
    return root


def best_move(root):
    """Play the most-visited move, not the one with the best average."""
    return max(root.children, key=lambda ch: ch.n).move
