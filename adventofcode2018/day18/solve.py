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

    grid = [list(line) for line in lines if line]
    if not grid:
        print(0)
        print(0)
        return

    h = len(grid)
    w = len(grid[0])

    def step(g):
        ng = [row[:] for row in g]
        for y in range(h):
            for x in range(w):
                trees = 0
                lumber = 0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        ny = y + dy
                        nx = x + dx
                        if 0 <= ny < h and 0 <= nx < w:
                            if g[ny][nx] == '|':
                                trees += 1
                            elif g[ny][nx] == '#':
                                lumber += 1
                cur = g[y][x]
                if cur == '.':
                    if trees >= 3:
                        ng[y][x] = '|'
                elif cur == '|':
                    if lumber >= 3:
                        ng[y][x] = '#'
                else:  # '#'
                    if not (lumber >= 1 and trees >= 1):
                        ng[y][x] = '.'
        return ng

    def value(g):
        trees = 0
        lumber = 0
        for row in g:
            for ch in row:
                if ch == '|':
                    trees += 1
                elif ch == '#':
                    lumber += 1
        return trees * lumber

    g = grid
    part1 = None
    seen = {}
    t = 0
    target = 1_000_000_000

    while t < target:
        if t == 10:
            part1 = value(g)

        key = ''.join(''.join(r) for r in g)
        if key in seen:
            cycle_start = seen[key]
            cycle_len = t - cycle_start
            remaining = target - t
            skip = remaining // cycle_len
            if skip > 0:
                t += skip * cycle_len
                continue
        else:
            seen[key] = t

        g = step(g)
        t += 1

    print(part1 if part1 is not None else value(grid))
    print(value(g))

if __name__ == '__main__':
    solve()
