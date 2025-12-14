import sys
import bisect

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

    galaxies = []
    for y in range(H):
        for x in range(W):
            if grid[y][x] == '#':
                galaxies.append((x, y))

    empty_rows = [y for y in range(H) if '#' not in grid[y]]
    empty_cols = []
    for x in range(W):
        if all(grid[y][x] != '#' for y in range(H)):
            empty_cols.append(x)

    def expanded_coords(factor):
        mul = factor - 1
        out = []
        for x, y in galaxies:
            dx = bisect.bisect_left(empty_cols, x)
            dy = bisect.bisect_left(empty_rows, y)
            out.append((x + mul * dx, y + mul * dy))
        return out

    def sum_pairwise(coords):
        xs = sorted(x for x, y in coords)
        ys = sorted(y for x, y in coords)

        def one(arr):
            pref = 0
            total = 0
            for i, v in enumerate(arr):
                total += v * i - pref
                pref += v
            return total

        return one(xs) + one(ys)

    part1 = sum_pairwise(expanded_coords(2))
    part2 = sum_pairwise(expanded_coords(1_000_000))
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
