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
    grid = [s for s in lines if s]
    if not grid:
        print(0)
        print(0)
        return

    H = len(grid)
    W = len(grid[0])
    a = [list(row) for row in grid]

    step = 0
    while True:
        step += 1
        moved = False

        b = [row[:] for row in a]
        for y in range(H):
            for x in range(W):
                if a[y][x] == '>':
                    nx = (x + 1) % W
                    if a[y][nx] == '.':
                        b[y][x] = '.'
                        b[y][nx] = '>'
                        moved = True
        a = b

        b = [row[:] for row in a]
        for y in range(H):
            for x in range(W):
                if a[y][x] == 'v':
                    ny = (y + 1) % H
                    if a[ny][x] == '.':
                        b[y][x] = '.'
                        b[ny][x] = 'v'
                        moved = True
        a = b

        if not moved:
            break

    print(step)
    print(0)

if __name__ == '__main__':
    solve()
