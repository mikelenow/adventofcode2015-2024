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
    rules = {}

    def rotate(grid):
        n = len(grid)
        return [''.join(grid[n - 1 - r][c] for r in range(n)) for c in range(n)]

    def flip(grid):
        return [row[::-1] for row in grid]

    def variants(grid):
        seen = set()
        cur = grid
        for _ in range(4):
            t = tuple(cur)
            if t not in seen:
                seen.add(t)
            f = tuple(flip(cur))
            if f not in seen:
                seen.add(f)
            cur = rotate(cur)
        return [list(v) for v in seen]

    for line in lines:
        if not line:
            continue
        src, dst = line.split(' => ')
        src_grid = src.split('/')
        dst_grid = dst.split('/')
        for v in variants(src_grid):
            rules['/'.join(v)] = dst_grid

    grid = ['.#.', '..#', '###']

    def step(grid):
        size = len(grid)
        if size % 2 == 0:
            block = 2
            out_block = 3
        else:
            block = 3
            out_block = 4

        new_size = size // block * out_block
        new_grid = [''] * new_size

        for by in range(0, size, block):
            for bx in range(0, size, block):
                sub = [grid[by + r][bx:bx + block] for r in range(block)]
                key = '/'.join(sub)
                out = rules[key]
                ty = (by // block) * out_block
                tx = (bx // block) * out_block
                for r in range(out_block):
                    new_grid[ty + r] += out[r]
        return new_grid

    part1 = 0
    part2 = 0
    for i in range(18):
        grid = step(grid)
        if i == 4:
            part1 = sum(row.count('#') for row in grid)
    part2 = sum(row.count('#') for row in grid)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
