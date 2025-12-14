import sys
import re

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
    valves = {}
    flows = {}
    for s in lines:
        if not s:
            continue
        m = re.match(r"^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)$", s)
        if not m:
            continue
        v = m.group(1)
        f = int(m.group(2))
        outs = [x.strip() for x in m.group(3).split(',')]
        valves[v] = outs
        flows[v] = f

    if 'AA' not in valves:
        print(0)
        print(0)
        return

    useful = [v for v, f in flows.items() if f > 0]
    useful.sort()
    idx = {v: i for i, v in enumerate(useful)}

    from collections import deque

    def bfs(src):
        dist = {src: 0}
        dq = deque([src])
        while dq:
            u = dq.popleft()
            for w in valves.get(u, []):
                if w not in dist:
                    dist[w] = dist[u] + 1
                    dq.append(w)
        return dist

    nodes = ['AA'] + useful
    dists = {}
    for n in nodes:
        dists[n] = bfs(n)

    rel = {}
    for a in nodes:
        rel[a] = {}
        for b in useful:
            if a == b:
                continue
            if b in dists[a]:
                rel[a][b] = dists[a][b]

    N = len(useful)

    from functools import lru_cache

    @lru_cache(None)
    def best(pos, time_left, opened_mask):
        ans = 0
        for v in useful:
            bit = 1 << idx[v]
            if opened_mask & bit:
                continue
            d = rel[pos].get(v)
            if d is None:
                continue
            nt = time_left - d - 1
            if nt <= 0:
                continue
            gain = flows[v] * nt
            ans = max(ans, gain + best(v, nt, opened_mask | bit))
        return ans

    part1 = best('AA', 30, 0)

    best_mask = [0] * (1 << N)

    def explore(pos, time_left, opened_mask, score):
        if score > best_mask[opened_mask]:
            best_mask[opened_mask] = score
        for v in useful:
            bit = 1 << idx[v]
            if opened_mask & bit:
                continue
            d = rel[pos].get(v)
            if d is None:
                continue
            nt = time_left - d - 1
            if nt <= 0:
                continue
            explore(v, nt, opened_mask | bit, score + flows[v] * nt)

    explore('AA', 26, 0, 0)

    for i in range(N):
        bit = 1 << i
        for m in range(1 << N):
            if m & bit:
                a = best_mask[m]
                b = best_mask[m ^ bit]
                if b > a:
                    best_mask[m] = b

    full = (1 << N) - 1
    part2 = 0
    for m in range(1 << N):
        part2 = max(part2, best_mask[m] + best_mask[full ^ m])

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
