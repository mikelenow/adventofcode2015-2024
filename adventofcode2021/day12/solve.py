import sys
from functools import lru_cache

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
    edges = []
    for s in lines:
        if not s:
            continue
        a, b = s.split('-')
        edges.append((a, b))

    if not edges:
        print(0)
        print(0)
        return

    names = set()
    for a, b in edges:
        names.add(a)
        names.add(b)
    names = sorted(names)
    idx = {name: i for i, name in enumerate(names)}

    n = len(names)
    g = [[] for _ in range(n)]
    for a, b in edges:
        ia = idx[a]
        ib = idx[b]
        g[ia].append(ib)
        g[ib].append(ia)

    start = idx['start']
    end = idx['end']

    is_small = [name.islower() for name in names]
    small_id = {}
    small_list = []
    for i, name in enumerate(names):
        if is_small[i] and name not in ('start', 'end'):
            small_id[i] = len(small_list)
            small_list.append(i)

    @lru_cache(None)
    def dfs1(v, mask):
        if v == end:
            return 1
        total = 0
        for w in g[v]:
            if w == start:
                continue
            if is_small[w]:
                if w == end:
                    total += dfs1(w, mask)
                else:
                    sid = small_id.get(w)
                    if sid is None:
                        total += dfs1(w, mask)
                    else:
                        bit = 1 << sid
                        if mask & bit:
                            continue
                        total += dfs1(w, mask | bit)
            else:
                total += dfs1(w, mask)
        return total

    @lru_cache(None)
    def dfs2(v, mask, used_twice):
        if v == end:
            return 1
        total = 0
        for w in g[v]:
            if w == start:
                continue
            if is_small[w]:
                if w == end:
                    total += dfs2(w, mask, used_twice)
                else:
                    sid = small_id.get(w)
                    if sid is None:
                        total += dfs2(w, mask, used_twice)
                    else:
                        bit = 1 << sid
                        if mask & bit:
                            if used_twice:
                                continue
                            total += dfs2(w, mask, True)
                        else:
                            total += dfs2(w, mask | bit, used_twice)
            else:
                total += dfs2(w, mask, used_twice)
        return total

    print(dfs1(start, 0))
    print(dfs2(start, 0, False))

if __name__ == '__main__':
    solve()
