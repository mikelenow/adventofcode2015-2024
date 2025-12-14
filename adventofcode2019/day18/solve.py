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
    grid = [list(line.rstrip('\n')) for line in lines if line.rstrip('\n')]
    if not grid:
        print(0)
        print(0)
        return

    h = len(grid)
    w = max(len(r) for r in grid)
    for r in grid:
        if len(r) < w:
            r.extend(['#'] * (w - len(r)))

    def solve_map(g):
        starts = []
        keys = {}
        for y in range(len(g)):
            for x in range(len(g[0])):
                ch = g[y][x]
                if ch == '@':
                    starts.append((x, y))
                elif 'a' <= ch <= 'z':
                    keys[ch] = (x, y)

        key_list = sorted(keys.keys())
        key_index = {k: i for i, k in enumerate(key_list)}
        all_mask = (1 << len(key_list)) - 1

        def is_open(x, y):
            c = g[y][x]
            return c != '#'

        def add_mask(store, cell, mask):
            cur = store.get(cell)
            if cur is None:
                store[cell] = [mask]
                return True
            for m in cur:
                if (m & mask) == m:
                    return False
            new = []
            for m in cur:
                if not ((mask & m) == mask):
                    new.append(m)
            new.append(mask)
            store[cell] = new
            return True

        from collections import deque

        def bfs_from(src):
            q = deque()
            q.append((src[0], src[1], 0, 0))
            seen = {}
            add_mask(seen, (src[0], src[1]), 0)
            found = []
            while q:
                x, y, d, req = q.popleft()
                for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                    nx, ny = x + dx, y + dy
                    if nx < 0 or ny < 0 or nx >= w or ny >= h:
                        continue
                    c = g[ny][nx]
                    if c == '#':
                        continue
                    nreq = req
                    if 'A' <= c <= 'Z':
                        nreq |= 1 << key_index.get(c.lower(), 31)
                    if add_mask(seen, (nx, ny), nreq):
                        q.append((nx, ny, d + 1, nreq))
                    if 'a' <= c <= 'z':
                        found.append((c, d + 1, nreq))
            best = {}
            for k, d, req in found:
                prev = best.get(k)
                if prev is None:
                    best[k] = (d, req)
                else:
                    pd, preq = prev
                    if d < pd or (d == pd and (req & preq) == req):
                        best[k] = (d, req)
            return [(k, d, req) for k, (d, req) in best.items()]

        nodes = []
        nodes.extend(starts)
        for k in key_list:
            nodes.append(keys[k])

        edges = {i: [] for i in range(len(nodes))}
        for i, pos in enumerate(nodes):
            for k, dist, req in bfs_from(pos):
                ki = key_index[k]
                edges[i].append((ki, dist, req))

        import heapq

        if len(starts) == 1:
            start_state = (0, 0)
            pq = [(0, start_state)]
            best = {start_state: 0}
            while pq:
                d, (pos_idx, mask) = heapq.heappop(pq)
                if d != best.get((pos_idx, mask)):
                    continue
                if mask == all_mask:
                    return d
                for ki, dist, req in edges[pos_idx]:
                    bit = 1 << ki
                    if mask & bit:
                        continue
                    if req & ~mask:
                        continue
                    nmask = mask | bit
                    npos = 1 + ki
                    nd = d + dist
                    st = (npos, nmask)
                    if nd < best.get(st, 10**18):
                        best[st] = nd
                        heapq.heappush(pq, (nd, st))
            return 0

        start_positions = tuple(range(len(starts)))
        start_state = (start_positions, 0)
        pq = [(0, start_state)]
        best = {start_state: 0}
        while pq:
            d, (poses, mask) = heapq.heappop(pq)
            if d != best.get((poses, mask)):
                continue
            if mask == all_mask:
                return d
            for ri in range(len(poses)):
                pos_idx = poses[ri]
                for ki, dist, req in edges[pos_idx]:
                    bit = 1 << ki
                    if mask & bit:
                        continue
                    if req & ~mask:
                        continue
                    nmask = mask | bit
                    nposes = list(poses)
                    nposes[ri] = len(starts) + ki
                    nposes = tuple(nposes)
                    nd = d + dist
                    st = (nposes, nmask)
                    if nd < best.get(st, 10**18):
                        best[st] = nd
                        heapq.heappush(pq, (nd, st))
        return 0

    part1 = solve_map([row[:] for row in grid])

    g2 = [row[:] for row in grid]
    sx = sy = None
    for y in range(h):
        for x in range(w):
            if g2[y][x] == '@':
                sx, sy = x, y
                break
        if sx is not None:
            break
    if sx is None:
        part2 = 0
    else:
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            g2[sy + dy][sx + dx] = '#'
        for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            g2[sy + dy][sx + dx] = '@'
        part2 = solve_map(g2)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
