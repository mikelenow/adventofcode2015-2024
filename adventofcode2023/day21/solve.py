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
    grid = [line for line in lines if line]
    H = len(grid)
    W = len(grid[0]) if H else 0

    if H == 0 or W == 0:
        print(0)
        print(0)
        return

    sx = sy = None
    for y in range(H):
        x = grid[y].find('S')
        if x != -1:
            sx, sy = x, y
            break
    if sx is None:
        print(0)
        print(0)
        return

    def neigh4(x, y):
        yield x + 1, y
        yield x - 1, y
        yield x, y + 1
        yield x, y - 1

    def part1_count(steps):
        cur = {(sx, sy)}
        for _ in range(steps):
            nxt = set()
            for x, y in cur:
                for nx, ny in neigh4(x, y):
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] != '#':
                        nxt.add((nx, ny))
            cur = nxt
        return len(cur)

    part1 = part1_count(64)

    def is_open_inf(rx, ry):
        return grid[(ry + sy) % H][(rx + sx) % W] != '#'

    def count_inf(steps):
        cur = {(0, 0)}
        for _ in range(steps):
            nxt = set()
            for x, y in cur:
                for nx, ny in neigh4(x, y):
                    if is_open_inf(nx, ny):
                        nxt.add((nx, ny))
            cur = nxt
        return len(cur)

    # AoC 2023 Day 21 part 2 relies on the fact that for n = offset + k*H
    # the reachable count becomes a quadratic in k for the given puzzle input.
    big = 26501365
    offset = big % H
    s0 = offset
    s1 = offset + H
    s2 = offset + 2 * H
    y0 = count_inf(s0)
    y1 = count_inf(s1)
    y2 = count_inf(s2)

    # Fit f(k) = a*k^2 + b*k + c
    c = y0
    a = (y2 - 2 * y1 + y0) // 2
    b = y1 - y0 - a
    k = (big - offset) // H
    part2 = a * k * k + b * k + c

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
