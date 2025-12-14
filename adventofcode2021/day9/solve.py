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
    a = [[int(ch) for ch in row] for row in grid]

    lows = []
    part1 = 0
    for y in range(H):
        for x in range(W):
            v = a[y][x]
            ok = True
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx = x + dx
                ny = y + dy
                if 0 <= nx < W and 0 <= ny < H:
                    if a[ny][nx] <= v:
                        ok = False
                        break
            if ok:
                lows.append((x, y))
                part1 += v + 1

    seen = set()
    sizes = []
    for sx, sy in lows:
        if (sx, sy) in seen:
            continue
        stack = [(sx, sy)]
        seen.add((sx, sy))
        sz = 0
        while stack:
            x, y = stack.pop()
            sz += 1
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx = x + dx
                ny = y + dy
                if 0 <= nx < W and 0 <= ny < H:
                    if (nx, ny) not in seen and a[ny][nx] != 9:
                        seen.add((nx, ny))
                        stack.append((nx, ny))
        sizes.append(sz)

    sizes.sort(reverse=True)
    part2 = sizes[0] * sizes[1] * sizes[2] if len(sizes) >= 3 else 0

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
