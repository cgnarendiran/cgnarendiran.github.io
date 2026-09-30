"""Plain MCTS on a 7x7 Go life-and-death position (Figure 2 of part 1).

Black's corner group (A2 B2 C2 D2 D1) has three empty points inside it: A1 B1 C1.
Black at B1 makes two eyes and lives; White at B1 kills it. The rest of the board
is settled so that the corner decides the game under area scoring. Black to move.

    python3 go7x7.py            # 5,000 simulations, about six seconds
"""
import sys
from mcts import uct_search, best_move

S = 7
N = S * S
EMPTY, BLACK, WHITE = 0, 1, 2
COLS = "ABCDEFG"
NBR = [[] for _ in range(N)]
for r in range(S):
    for c in range(S):
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= r + dr < S and 0 <= c + dc < S:
                NBR[r * S + c].append((r + dr) * S + c + dc)


def idx(name):
    return (int(name[1:]) - 1) * S + COLS.index(name[0])


def name(i):
    return "pass" if i is None else f"{COLS[i % S]}{i // S + 1}"


def group(b, i):
    """The stones connected to i, and their empty neighbours (liberties)."""
    stack, stones, libs = [i], {i}, set()
    while stack:
        j = stack.pop()
        for k in NBR[j]:
            if b[k] == EMPTY:
                libs.add(k)
            elif b[k] == b[i] and k not in stones:
                stones.add(k)
                stack.append(k)
    return stones, libs


class Go:
    def __init__(self, board, to_move=BLACK, ko=None, passes=0):
        self.b, self.to, self.ko, self.passes = board, to_move, ko, passes

    @classmethod
    def puzzle(cls):
        b = [EMPTY] * N
        for p in "A2 B2 C2 D2 D1".split():
            b[idx(p)] = BLACK
        for p in "A3 B3 C3 D3 E3 E2 E1".split():
            b[idx(p)] = WHITE
        for c in COLS:
            b[idx(c + "4")] = WHITE
            b[idx(c + "5")] = BLACK
        return cls(b)

    # ---- the five methods mcts.py needs
    def copy(self):
        return Go(self.b[:], self.to, self.ko, self.passes)

    def legal_moves(self):
        """Legal moves that don't fill the mover's own eye; pass only if there are none."""
        moves = [i for i in range(N) if self.b[i] == EMPTY and not self.own_eye(i)
                 and self.copy().try_play(i)]
        return moves or [None]

    def play(self, move):
        assert self.try_play(move)

    def is_over(self):
        return self.passes >= 2

    def first_to_move(self):
        return self.to == BLACK

    # ---- Go rules
    def own_eye(self, i):
        return all(self.b[k] == self.to for k in NBR[i])

    def try_play(self, i):
        """Play at i (None passes). Returns False and changes nothing if illegal."""
        if i is None:
            self.to, self.ko, self.passes = 3 - self.to, None, self.passes + 1
            return True
        b, me, opp = self.b, self.to, 3 - self.to
        if b[i] != EMPTY or i == self.ko:
            return False
        b[i] = me
        captured = []
        for k in NBR[i]:
            if b[k] == opp:
                stones, libs = group(b, k)
                if not libs:
                    captured.extend(stones)
                    for s in stones:
                        b[s] = EMPTY
        mine, libs = group(b, i)
        if not libs:  # suicide: undo
            b[i] = EMPTY
            for s in captured:
                b[s] = opp
            return False
        single = len(captured) == 1 and len(mine) == 1 and len(libs) == 1
        self.ko = captured[0] if single else None
        self.to, self.passes = opp, 0
        return True

    def black_wins(self, komi=0.5):
        """Area scoring: stones plus empty points surrounded by one colour."""
        score = -komi
        for i in range(N):
            if self.b[i] == EMPTY:
                around = {self.b[k] for k in NBR[i]} - {EMPTY}
                owner = around.pop() if len(around) == 1 else EMPTY
            else:
                owner = self.b[i]
            score += (owner == BLACK) - (owner == WHITE)
        return score > 0


def rollout(state, rng):
    """Random moves (never filling your own eye) until both sides pass."""
    for _ in range(3 * N):
        if state.passes >= 2:
            break
        empties = [i for i in range(N) if state.b[i] == EMPTY and not state.own_eye(i)]
        rng.shuffle(empties)
        if not any(state.try_play(i) for i in empties):
            state.try_play(None)
    return 1.0 if state.black_wins() else 0.0


if __name__ == "__main__":
    sims = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    root = uct_search(Go.puzzle(), rollout, sims, c=1.0, seed=0)
    for ch in sorted(root.children, key=lambda ch: -ch.n)[:6]:
        print(f"{name(ch.move):5s} visits {ch.n:5d}   wins {ch.w / ch.n:.0%}")
    print("play:", name(best_move(root)))
