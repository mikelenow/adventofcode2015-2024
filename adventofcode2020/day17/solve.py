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
    grid = [s for s in lines if s]
    if not grid:
        print(0)
        print(0)
        return

    active3 = set()
    active4 = set()
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == '#':
                active3.add((x, y, 0))
                active4.add((x, y, 0, 0))

    neigh3 = [(dx, dy, dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1) if not (dx == dy == dz == 0)]
    neigh4 = [(dx, dy, dz, dw) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1) for dw in (-1, 0, 1) if not (dx == dy == dz == dw == 0)]

    def step3(act):
        cnt = defaultdict(int)
        for x, y, z in act:
            for dx, dy, dz in neigh3:
                cnt[(x + dx, y + dy, z + dz)] += 1
        out = set()
        for p, n in cnt.items():
            if p in act:
                if n == 2 or n == 3:
                    out.add(p)
            else:
                if n == 3:
                    out.add(p)
        return out

    def step4(act):
        cnt = defaultdict(int)
        for x, y, z, w in act:
            for dx, dy, dz, dw in neigh4:
                cnt[(x + dx, y + dy, z + dz, w + dw)] += 1
        out = set()
        for p, n in cnt.items():
            if p in act:
                if n == 2 or n == 3:
                    out.add(p)
            else:
                if n == 3:
                    out.add(p)
        return out

    for _ in range(6):
        active3 = step3(active3)
        active4 = step4(active4)

    print(len(active3))
    print(len(active4))

if __name__ == '__main__':
    solve()
