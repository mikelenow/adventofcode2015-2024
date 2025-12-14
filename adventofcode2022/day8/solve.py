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
    grid = [list(map(int, s)) for s in lines if s]
    if not grid:
        print(0)
        print(0)
        return

    H = len(grid)
    W = len(grid[0])

    left_max = [[-1] * W for _ in range(H)]
    right_max = [[-1] * W for _ in range(H)]
    up_max = [[-1] * W for _ in range(H)]
    down_max = [[-1] * W for _ in range(H)]

    for y in range(H):
        m = -1
        for x in range(W):
            left_max[y][x] = m
            m = max(m, grid[y][x])
        m = -1
        for x in range(W - 1, -1, -1):
            right_max[y][x] = m
            m = max(m, grid[y][x])

    for x in range(W):
        m = -1
        for y in range(H):
            up_max[y][x] = m
            m = max(m, grid[y][x])
        m = -1
        for y in range(H - 1, -1, -1):
            down_max[y][x] = m
            m = max(m, grid[y][x])

    visible = 0
    for y in range(H):
        for x in range(W):
            h = grid[y][x]
            if h > left_max[y][x] or h > right_max[y][x] or h > up_max[y][x] or h > down_max[y][x]:
                visible += 1

    best = 0
    for y in range(H):
        for x in range(W):
            h = grid[y][x]
            a = 0
            for xx in range(x - 1, -1, -1):
                a += 1
                if grid[y][xx] >= h:
                    break
            b = 0
            for xx in range(x + 1, W):
                b += 1
                if grid[y][xx] >= h:
                    break
            c = 0
            for yy in range(y - 1, -1, -1):
                c += 1
                if grid[yy][x] >= h:
                    break
            d = 0
            for yy in range(y + 1, H):
                d += 1
                if grid[yy][x] >= h:
                    break
            best = max(best, a * b * c * d)

    print(visible)
    print(best)

if __name__ == '__main__':
    solve()
