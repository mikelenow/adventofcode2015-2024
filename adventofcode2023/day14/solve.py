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
    grid0 = [list(line) for line in lines if line]
    H = len(grid0)
    W = len(grid0[0]) if H else 0

    def load(g):
        total = 0
        for y in range(H):
            for x in range(W):
                if g[y][x] == 'O':
                    total += H - y
        return total

    def tilt_north(g):
        for x in range(W):
            w = 0
            for y in range(H):
                if g[y][x] == '#':
                    w = y + 1
                elif g[y][x] == 'O':
                    if y != w:
                        g[y][x] = '.'
                        g[w][x] = 'O'
                    w += 1

    def tilt_south(g):
        for x in range(W):
            w = H - 1
            for y in range(H - 1, -1, -1):
                if g[y][x] == '#':
                    w = y - 1
                elif g[y][x] == 'O':
                    if y != w:
                        g[y][x] = '.'
                        g[w][x] = 'O'
                    w -= 1

    def tilt_west(g):
        for y in range(H):
            w = 0
            for x in range(W):
                if g[y][x] == '#':
                    w = x + 1
                elif g[y][x] == 'O':
                    if x != w:
                        g[y][x] = '.'
                        g[y][w] = 'O'
                    w += 1

    def tilt_east(g):
        for y in range(H):
            w = W - 1
            for x in range(W - 1, -1, -1):
                if g[y][x] == '#':
                    w = x - 1
                elif g[y][x] == 'O':
                    if x != w:
                        g[y][x] = '.'
                        g[y][w] = 'O'
                    w -= 1

    g1 = [row[:] for row in grid0]
    tilt_north(g1)
    part1 = load(g1)

    def state(g):
        return tuple(''.join(r) for r in g)

    g = [row[:] for row in grid0]
    seen = {}
    order = []
    i = 0
    target = 1_000_000_000
    while i < target:
        s = state(g)
        if s in seen:
            start = seen[s]
            cycle = i - start
            rem = (target - start) % cycle
            g = [list(r) for r in order[start + rem]]
            break
        seen[s] = i
        order.append(s)

        tilt_north(g)
        tilt_west(g)
        tilt_south(g)
        tilt_east(g)
        i += 1

    part2 = load(g)
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
