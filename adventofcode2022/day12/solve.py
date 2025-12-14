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
    start = None
    end = None
    hgt = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            ch = grid[y][x]
            if ch == 'S':
                start = (x, y)
                ch2 = 'a'
            elif ch == 'E':
                end = (x, y)
                ch2 = 'z'
            else:
                ch2 = ch
            hgt[y][x] = ord(ch2) - 97

    if start is None or end is None:
        print(0)
        print(0)
        return

    from collections import deque

    dist = [[-1] * W for _ in range(H)]
    ex, ey = end
    dist[ey][ex] = 0
    dq = deque([(ex, ey)])
    while dq:
        x, y = dq.popleft()
        d = dist[y][x]
        h = hgt[y][x]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx = x + dx
            ny = y + dy
            if not (0 <= nx < W and 0 <= ny < H):
                continue
            if dist[ny][nx] != -1:
                continue
            nh = hgt[ny][nx]
            if nh >= h - 1:
                dist[ny][nx] = d + 1
                dq.append((nx, ny))

    sx, sy = start
    part1 = dist[sy][sx]
    best = None
    for y in range(H):
        for x in range(W):
            if hgt[y][x] == 0 and dist[y][x] != -1:
                if best is None or dist[y][x] < best:
                    best = dist[y][x]
    part2 = best if best is not None else 0

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
