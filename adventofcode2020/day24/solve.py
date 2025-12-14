import sys
from collections import defaultdict

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
    dirs = {
        'e': (1, 0),
        'w': (-1, 0),
        'ne': (1, -1),
        'nw': (0, -1),
        'se': (0, 1),
        'sw': (-1, 1),
    }

    black = set()
    for s in lines:
        if not s:
            continue
        i = 0
        x = 0
        y = 0
        while i < len(s):
            if s[i] in ('e', 'w'):
                d = s[i]
                i += 1
            else:
                d = s[i:i + 2]
                i += 2
            dx, dy = dirs[d]
            x += dx
            y += dy
        p = (x, y)
        if p in black:
            black.remove(p)
        else:
            black.add(p)

    part1 = len(black)

    neigh = list(dirs.values())
    for _ in range(100):
        cnt = defaultdict(int)
        for x, y in black:
            for dx, dy in neigh:
                cnt[(x + dx, y + dy)] += 1
        new_black = set()
        for p, n in cnt.items():
            if p in black:
                if n == 1 or n == 2:
                    new_black.add(p)
            else:
                if n == 2:
                    new_black.add(p)
        black = new_black

    part2 = len(black)
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
