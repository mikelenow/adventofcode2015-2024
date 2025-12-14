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
    grid0 = [s for s in lines if s]
    if not grid0:
        print(0)
        print(0)
        return

    h = len(grid0)
    w = len(grid0[0])

    def step_adj(grid):
        out = [list(row) for row in grid]
        changed = False
        for y in range(h):
            for x in range(w):
                c = grid[y][x]
                if c == '.':
                    continue
                occ = 0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        ny = y + dy
                        nx = x + dx
                        if 0 <= ny < h and 0 <= nx < w and grid[ny][nx] == '#':
                            occ += 1
                if c == 'L' and occ == 0:
                    out[y][x] = '#'
                    changed = True
                elif c == '#' and occ >= 4:
                    out[y][x] = 'L'
                    changed = True
        return [''.join(r) for r in out], changed

    def step_vis(grid, vis):
        out = [list(row) for row in grid]
        changed = False
        for y in range(h):
            for x in range(w):
                c = grid[y][x]
                if c == '.':
                    continue
                occ = 0
                for ny, nx in vis[(y, x)]:
                    if grid[ny][nx] == '#':
                        occ += 1
                if c == 'L' and occ == 0:
                    out[y][x] = '#'
                    changed = True
                elif c == '#' and occ >= 5:
                    out[y][x] = 'L'
                    changed = True
        return [''.join(r) for r in out], changed

    g = grid0
    while True:
        g2, ch = step_adj(g)
        g = g2
        if not ch:
            break
    part1 = sum(row.count('#') for row in g)

    vis = {}
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for y in range(h):
        for x in range(w):
            if grid0[y][x] == '.':
                continue
            lst = []
            for dx, dy in dirs:
                nx = x + dx
                ny = y + dy
                while 0 <= ny < h and 0 <= nx < w and grid0[ny][nx] == '.':
                    nx += dx
                    ny += dy
                if 0 <= ny < h and 0 <= nx < w and grid0[ny][nx] != '.':
                    lst.append((ny, nx))
            vis[(y, x)] = lst

    g = grid0
    while True:
        g2, ch = step_vis(g, vis)
        g = g2
        if not ch:
            break
    part2 = sum(row.count('#') for row in g)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
