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
    g = {}
    for line in lines:
        if not line:
            continue
        a, rest = line.split(':')
        a = a.strip()
        bs = rest.strip().split()
        g.setdefault(a, {})
        for b in bs:
            g.setdefault(b, {})
            g[a][b] = g[a].get(b, 0) + 1
            g[b][a] = g[b].get(a, 0) + 1

    # Stoer-Wagner minimum cut with partition recovery.
    nodes = list(g.keys())
    comp = {v: {v} for v in nodes}

    best_cut = 10**18
    best_part = None

    adj = {u: dict(vs) for u, vs in g.items()}
    verts = list(adj.keys())

    while len(verts) > 1:
        used = set()
        weights = {v: 0 for v in verts}
        prev = None
        last = None

        for _ in range(len(verts)):
            sel = max((v for v in verts if v not in used), key=lambda v: weights[v])
            used.add(sel)
            prev, last = last, sel
            for nb, w in adj[sel].items():
                if nb not in used:
                    weights[nb] += w

        cut_w = weights[last]
        if cut_w < best_cut:
            best_cut = cut_w
            part = comp[last]
            best_part = (set(part), set().union(*[comp[v] for v in verts if v != last]))

        # merge last into prev
        if prev is None:
            break

        for nb, w in list(adj[last].items()):
            if nb == prev:
                continue
            adj[prev][nb] = adj[prev].get(nb, 0) + w
            adj[nb][prev] = adj[prev][nb]
            adj[nb].pop(last, None)
        adj[prev].pop(last, None)
        del adj[last]

        comp[prev] |= comp[last]
        del comp[last]
        verts.remove(last)

    part1 = 0
    if best_part is not None and best_cut == 3:
        part1 = len(best_part[0]) * len(best_part[1])

    print(part1)
    print(0)

if __name__ == '__main__':
    solve()
