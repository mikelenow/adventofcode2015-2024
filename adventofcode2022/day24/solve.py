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

    start = (grid[0].index('.'), 0)
    end = (grid[-1].index('.'), H - 1)

    blz = []
    for y in range(H):
        for x in range(W):
            ch = grid[y][x]
            if ch in '<>^v':
                blz.append((x, y, ch))

    inner_w = W - 2
    inner_h = H - 2
    from math import gcd
    period = inner_w * inner_h // gcd(inner_w, inner_h)

    blocked = [set() for _ in range(period)]
    for t in range(period):
        s = set()
        for x0, y0, ch in blz:
            if ch == '>':
                x = 1 + ((x0 - 1 + t) % inner_w)
                y = y0
            elif ch == '<':
                x = 1 + ((x0 - 1 - t) % inner_w)
                y = y0
            elif ch == 'v':
                x = x0
                y = 1 + ((y0 - 1 + t) % inner_h)
            else:
                x = x0
                y = 1 + ((y0 - 1 - t) % inner_h)
            s.add((x, y))
        blocked[t] = s

    from collections import deque

    def bfs(t0, src, dst):
        q = deque()
        seen = set()
        q.append((src[0], src[1], t0))
        seen.add((src[0], src[1], t0 % period))
        while q:
            x, y, t = q.popleft()
            if (x, y) == dst:
                return t
            nt = t + 1
            b = blocked[nt % period]
            for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx = x + dx
                ny = y + dy
                if (nx, ny) == dst or (nx, ny) == src:
                    if (nx, ny) not in b:
                        key = (nx, ny, nt % period)
                        if key not in seen:
                            seen.add(key)
                            q.append((nx, ny, nt))
                    continue
                if nx <= 0 or nx >= W - 1 or ny <= 0 or ny >= H - 1:
                    continue
                if (nx, ny) in b:
                    continue
                key = (nx, ny, nt % period)
                if key in seen:
                    continue
                seen.add(key)
                q.append((nx, ny, nt))
        return 0

    t1 = bfs(0, start, end)
    t2 = bfs(t1, end, start)
    t3 = bfs(t2, start, end)

    print(t1)
    print(t3)

if __name__ == '__main__':
    solve()
