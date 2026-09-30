"""AlphaZero-style search (PUCT) for two-player games: mcts.py with a network.

Same game interface as mcts.py. Instead of a rollout you pass network(state),
which returns (priors, result): a probability for each legal move, and how good
the position is for the first player, between 0 and 1. For a finished game it
should return no priors and the real result. Explained in
https://cgnarendiran.github.io/blog/mcts-alphazero-part2/

    python3 puct.py     # a small demo on go7x7.py's position, a few seconds
"""
import math


class Node:
    def __init__(self, first_moved, move=None, parent=None, prior=1.0):
        self.move, self.parent, self.children = move, parent, []
        self.prior = prior                            # P(s,a), the network's guess
        self.first_moved = first_moved                # did the first player make `move`?
        self.n, self.w = 0, 0.0                       # visits, total result for that player


def puct_search(root_state, network, n_simulations, c_puct=1.5, on_step=None):
    root = Node(not root_state.first_to_move())
    for t in range(1, n_simulations + 1):
        node, state = root, root_state.copy()

        # 1. Select: walk down through expanded nodes by PUCT score
        while node.children:
            sqrt_n = math.sqrt(node.n)
            node = max(node.children,
                       key=lambda ch: (ch.w / ch.n if ch.n else 0.0)
                                      + c_puct * ch.prior * sqrt_n / (1 + ch.n))
            state.play(node.move)

        # 2. Expand: one network call gives every legal move its prior
        priors, result = network(state)
        node.children = [Node(state.first_to_move(), move, node, p)
                         for move, p in priors.items()]

        # 3. Evaluate: the same call scored the position, so there is no rollout

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


def visit_policy(root, tau=1.0):
    """The training label pi: each move's share of the visits, sharpened by tau."""
    weights = {ch.move: ch.n ** (1 / tau) for ch in root.children}
    total = sum(weights.values())
    return {move: w / total for move, w in weights.items()}


if __name__ == "__main__":
    # There is no trained network here, so a stand-in plays its part: one random
    # rollout gives the value, and the priors are either uniform (a network that
    # knows nothing) or lean on B1 (as a policy network that knew the shape would).
    import random
    from go7x7 import Go, idx, name, rollout

    def stand_in_network(hint=None, weight=0.5, seed=0):
        rng = random.Random(seed)

        def network(state):
            if state.is_over():
                return {}, 1.0 if state.black_wins() else 0.0
            moves = state.legal_moves()
            rng.shuffle(moves)  # so ties between unvisited moves don't favour board order
            share = 1 - weight if hint in moves else 1.0
            priors = {m: share / len(moves) for m in moves}
            if hint in moves:
                priors[hint] += weight
            return priors, rollout(state.copy(), rng)
        return network

    for label, hint in (("uniform priors", None), ("priors leaning on B1", idx("B1"))):
        last_behind = [0]  # the last simulation at which B1 was not the most-visited move

        def track(t, root):
            if best_move(root) != idx("B1"):
                last_behind[0] = t
        root = puct_search(Go.puzzle(), stand_in_network(hint), 1000, on_step=track)
        b1 = next(ch for ch in root.children if ch.move == idx("B1"))
        pi = visit_policy(root)
        print(f"{label:22s} B1 visits {b1.n:4d} of 1,000, wins {b1.w / b1.n:.0%}, "
              f"label pi(B1) = {pi[idx('B1')]:.2f}, top move for good from simulation {last_behind[0] + 1}")
