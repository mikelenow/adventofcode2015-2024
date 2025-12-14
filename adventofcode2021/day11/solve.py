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

    a = [[int(ch) for ch in row] for row in grid]
    H = len(a)
    W = len(a[0])

    def step():
        flashed = [[False] * W for _ in range(H)]
        stack = []
        for y in range(H):
            for x in range(W):
                a[y][x] += 1
                if a[y][x] > 9:
                    stack.append((x, y))

        cnt = 0
        while stack:
            x, y = stack.pop()
            if flashed[y][x]:
                continue
            if a[y][x] <= 9:
                continue
            flashed[y][x] = True
            cnt += 1
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        a[ny][nx] += 1
                        if a[ny][nx] > 9 and not flashed[ny][nx]:
                            stack.append((nx, ny))

        for y in range(H):
            for x in range(W):
                if flashed[y][x]:
                    a[y][x] = 0
        return cnt

    total = 0
    sync = None
    n_cells = H * W
    t = 0
    while sync is None or t < 100:
        t += 1
        c = step()
        if t <= 100:
            total += c
        if c == n_cells and sync is None:
            sync = t
    print(total)
    print(sync or 0)

if __name__ == '__main__':
    solve()
