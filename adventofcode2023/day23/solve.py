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

    grid = [line for line in lines if line]
    H = len(grid)
    W = len(grid[0]) if H else 0

    if H == 0 or W == 0:
        print(0)
        print(0)
        return

    start = (grid[0].index('.'), 0)
    end = (grid[H - 1].index('.'), H - 1)

    DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    slope_dir = {'>': (1, 0), 'v': (0, 1), '<': (-1, 0), '^': (0, -1)}

    def neighbors_any(x, y):
        out = []
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] != '#':
                out.append((nx, ny))
        return out

    def step_options(x, y, use_slopes):
        ch = grid[y][x]
        if use_slopes and ch in slope_dir:
            dx, dy = slope_dir[ch]
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] != '#':
                return [(nx, ny)]
            return []

        return neighbors_any(x, y)

    def build_graph(use_slopes):
        nodes = set([start, end])
        for y in range(H):
            for x in range(W):
                if grid[y][x] == '#':
                    continue
                deg = len(neighbors_any(x, y))
                if deg != 2:
                    nodes.add((x, y))

        nodes = list(nodes)
        node_set = set(nodes)
        idx = {p: i for i, p in enumerate(nodes)}
        g = [[] for _ in range(len(nodes))]

        for p in nodes:
            x, y = p
            pu = idx[p]
            best = {}
            for nx, ny in step_options(x, y, use_slopes):
                prev = (x, y)
                cur = (nx, ny)
                dist = 1
                seen_pairs = set()
                seen_pairs.add((prev, cur))
                while cur not in node_set:
                    cx, cy = cur
                    nxts = step_options(cx, cy, use_slopes)
                    if len(nxts) == 0:
                        break
                    if len(nxts) == 1:
                        ncur = nxts[0]
                    else:
                        if len(nxts) != 2:
                            break
                        a, b = nxts
                        ncur = b if a == prev else a
                    if (cur, ncur) in seen_pairs:
                        break
                    prev, cur = cur, ncur
                    seen_pairs.add((prev, cur))
                    dist += 1
                if cur in node_set:
                    v = idx[cur]
                    if v != pu:
                        old = best.get(v)
                        if old is None or dist > old:
                            best[v] = dist
            g[pu] = list(best.items())
        return g, idx[start], idx[end]

    def longest_path(graph, s, t):
        N = len(graph)
        seen = [False] * N
        best = 0

        def dfs(u, dist):
            nonlocal best
            if u == t:
                if dist > best:
                    best = dist
                return
            for v, w in graph[u]:
                if seen[v]:
                    continue
                seen[v] = True
                dfs(v, dist + w)
                seen[v] = False

        seen[s] = True
        dfs(s, 0)
        return best

    g1, s1, t1 = build_graph(True)
    part1 = longest_path(g1, s1, t1)

    g2, s2, t2 = build_graph(False)
    part2 = longest_path(g2, s2, t2)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
