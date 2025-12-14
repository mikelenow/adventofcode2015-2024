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
    segs = []
    for s in lines:
        if not s:
            continue
        a, b = s.split(' -> ')
        x1, y1 = (int(v) for v in a.split(','))
        x2, y2 = (int(v) for v in b.split(','))
        segs.append((x1, y1, x2, y2))

    def solve_for(include_diag):
        cnt = defaultdict(int)
        for x1, y1, x2, y2 in segs:
            dx = 0 if x1 == x2 else (1 if x2 > x1 else -1)
            dy = 0 if y1 == y2 else (1 if y2 > y1 else -1)
            if dx != 0 and dy != 0 and not include_diag:
                continue
            if dx != 0 and dy != 0 and abs(x2 - x1) != abs(y2 - y1):
                continue
            x = x1
            y = y1
            while True:
                cnt[(x, y)] += 1
                if x == x2 and y == y2:
                    break
                x += dx
                y += dy
        return sum(1 for v in cnt.values() if v >= 2)

    part1 = solve_for(False)
    part2 = solve_for(True)
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
