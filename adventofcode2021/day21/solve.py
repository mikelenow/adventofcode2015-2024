import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    # TODO: Implement solution
    vals = []
    for s in lines:
        if not s:
            continue
        vals.append(int(s.split(':')[-1].strip()))
    if len(vals) < 2:
        print(0)
        print(0)
        return

    p1, p2 = vals[0], vals[1]

    pos = [p1, p2]
    score = [0, 0]
    die = 1
    rolls = 0
    turn = 0
    while score[0] < 1000 and score[1] < 1000:
        move = 0
        for _ in range(3):
            move += die
            die += 1
            if die == 101:
                die = 1
            rolls += 1
        pos[turn] = ((pos[turn] - 1 + move) % 10) + 1
        score[turn] += pos[turn]
        turn ^= 1
    part1 = min(score) * rolls

    from functools import lru_cache

    outcomes = {}
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            for c in (1, 2, 3):
                outcomes[a + b + c] = outcomes.get(a + b + c, 0) + 1

    @lru_cache(None)
    def wins(p1, p2, s1, s2, turn):
        if s1 >= 21:
            return (1, 0)
        if s2 >= 21:
            return (0, 1)
        w1 = 0
        w2 = 0
        if turn == 0:
            for mv, mult in outcomes.items():
                np1 = ((p1 - 1 + mv) % 10) + 1
                a, b = wins(np1, p2, s1 + np1, s2, 1)
                w1 += a * mult
                w2 += b * mult
        else:
            for mv, mult in outcomes.items():
                np2 = ((p2 - 1 + mv) % 10) + 1
                a, b = wins(p1, np2, s1, s2 + np2, 0)
                w1 += a * mult
                w2 += b * mult
        return (w1, w2)

    w1, w2 = wins(p1, p2, 0, 0, 0)
    part2 = max(w1, w2)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
