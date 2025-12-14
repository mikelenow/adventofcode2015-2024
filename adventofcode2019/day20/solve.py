import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    # TODO: Implement solution
    raw = [line.rstrip('\n') for line in lines]
    if not raw:
        print(0)
        print(0)
        return

    w = max(len(r) for r in raw)
    grid = [list(r.ljust(w)) for r in raw]
    h = len(grid)

    def is_upper(c):
        return 'A' <= c <= 'Z'

    portals = {}
    start = None
    end = None

    for y in range(h):
        for x in range(w):
            if grid[y][x] != '.':
                continue
            label = None
            if y >= 2 and is_upper(grid[y - 2][x]) and is_upper(grid[y - 1][x]):
                label = grid[y - 2][x] + grid[y - 1][x]
            elif y + 2 < h and is_upper(grid[y + 1][x]) and is_upper(grid[y + 2][x]):
                label = grid[y + 1][x] + grid[y + 2][x]
            elif x >= 2 and is_upper(grid[y][x - 2]) and is_upper(grid[y][x - 1]):
                label = grid[y][x - 2] + grid[y][x - 1]
            elif x + 2 < w and is_upper(grid[y][x + 1]) and is_upper(grid[y][x + 2]):
                label = grid[y][x + 1] + grid[y][x + 2]
            if label is None:
                continue
            portals.setdefault(label, []).append((x, y))

    for label, ps in portals.items():
        if label == 'AA':
            start = ps[0]
        elif label == 'ZZ':
            end = ps[0]

    if start is None or end is None:
        print(0)
        print(0)
        return

    teleport = {}
    portal_type = {}
    for label, ps in portals.items():
        if label in ('AA', 'ZZ'):
            continue
        if len(ps) == 2:
            a, b = ps
            teleport[a] = b
            teleport[b] = a
            for p in (a, b):
                x, y = p
                outer = x <= 2 or y <= 2 or x >= w - 3 or y >= h - 3
                portal_type[p] = 'outer' if outer else 'inner'

    from collections import deque

    def bfs_flat():
        q = deque([(start, 0)])
        dist = {start: 0}
        while q:
            (x, y), d = q.popleft()
            if (x, y) == end:
                return d
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx >= w or ny >= h:
                    continue
                if grid[ny][nx] != '.':
                    continue
                if (nx, ny) not in dist:
                    dist[(nx, ny)] = d + 1
                    q.append(((nx, ny), d + 1))
            if (x, y) in teleport:
                nx, ny = teleport[(x, y)]
                if (nx, ny) not in dist:
                    dist[(nx, ny)] = d + 1
                    q.append(((nx, ny), d + 1))
        return 0

    def bfs_recursive():
        q = deque([((start[0], start[1], 0), 0)])
        dist = {(start[0], start[1], 0): 0}
        while q:
            (x, y, lv), d = q.popleft()
            if (x, y) == end and lv == 0:
                return d
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx >= w or ny >= h:
                    continue
                if grid[ny][nx] != '.':
                    continue
                st = (nx, ny, lv)
                if st not in dist:
                    dist[st] = d + 1
                    q.append((st, d + 1))
            pos = (x, y)
            if pos in teleport:
                tp = teleport[pos]
                t = portal_type.get(pos)
                if t == 'inner':
                    nl = lv + 1
                else:
                    if lv == 0:
                        nl = None
                    else:
                        nl = lv - 1
                if nl is not None:
                    st = (tp[0], tp[1], nl)
                    if st not in dist:
                        dist[st] = d + 1
                        q.append((st, d + 1))
        return 0

    part1 = bfs_flat()
    part2 = bfs_recursive()

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
