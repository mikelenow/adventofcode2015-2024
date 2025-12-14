import sys
from collections import deque

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
    blocks = []
    cur = []
    for s in lines + ['']:
        if s == '':
            if cur:
                blocks.append(cur)
            cur = []
        else:
            cur.append(s)

    if len(blocks) < 2:
        print(0)
        print(0)
        return

    p1 = deque(int(x) for x in blocks[0][1:] if x)
    p2 = deque(int(x) for x in blocks[1][1:] if x)

    def score(d):
        vals = list(d)
        vals.reverse()
        return sum((i + 1) * v for i, v in enumerate(vals))

    a = deque(p1)
    b = deque(p2)
    while a and b:
        x = a.popleft()
        y = b.popleft()
        if x > y:
            a.append(x)
            a.append(y)
        else:
            b.append(y)
            b.append(x)
    part1 = score(a if a else b)

    def rec_game(d1, d2):
        seen = set()
        while d1 and d2:
            key = (tuple(d1), tuple(d2))
            if key in seen:
                return 1, d1
            seen.add(key)
            x = d1.popleft()
            y = d2.popleft()
            if len(d1) >= x and len(d2) >= y:
                w, _ = rec_game(deque(list(d1)[:x]), deque(list(d2)[:y]))
            else:
                w = 1 if x > y else 2
            if w == 1:
                d1.append(x)
                d1.append(y)
            else:
                d2.append(y)
                d2.append(x)
        return (1, d1) if d1 else (2, d2)

    w, deck = rec_game(deque(p1), deque(p2))
    part2 = score(deck)
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
