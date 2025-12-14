import sys
import math
from collections import defaultdict

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
    blocks = []
    cur = []
    for s in lines + ['']:
        if s == '':
            if cur:
                blocks.append(cur)
            cur = []
        else:
            cur.append(s)

    tiles = {}
    for b in blocks:
        if not b:
            continue
        if not b[0].startswith('Tile '):
            continue
        tid = int(b[0][5:-1])
        grid = b[1:]
        tiles[tid] = grid

    if not tiles:
        print(0)
        print(0)
        return

    def rot90(g):
        h = len(g)
        w = len(g[0])
        return [''.join(g[h - 1 - r][c] for r in range(h)) for c in range(w)]

    def flip(g):
        return [row[::-1] for row in g]

    def orientations(g):
        res = []
        x = g
        for _ in range(4):
            res.append(x)
            x = rot90(x)
        x = flip(g)
        for _ in range(4):
            res.append(x)
            x = rot90(x)
        out = []
        seen = set()
        for gg in res:
            key = tuple(gg)
            if key not in seen:
                seen.add(key)
                out.append(gg)
        return out

    def edges(g):
        top = g[0]
        bottom = g[-1]
        left = ''.join(row[0] for row in g)
        right = ''.join(row[-1] for row in g)
        return top, bottom, left, right

    def canon(e):
        r = e[::-1]
        return e if e < r else r

    edge_count = defaultdict(int)
    tile_edges = {}
    for tid, g in tiles.items():
        t, b, l, r = edges(g)
        tile_edges[tid] = (t, b, l, r)
        for e in (t, b, l, r):
            edge_count[canon(e)] += 1

    corners = []
    for tid, (t, b, l, r) in tile_edges.items():
        uniq = sum(1 for e in (t, b, l, r) if edge_count[canon(e)] == 1)
        if uniq == 2:
            corners.append(tid)
    part1 = 1
    for tid in corners:
        part1 *= tid

    n_tiles = len(tiles)
    N = int(math.isqrt(n_tiles))
    if N * N != n_tiles:
        print(part1)
        print(0)
        return

    variants = {}
    for tid, g in tiles.items():
        vars_t = []
        for gg in orientations(g):
            t, b, l, r = edges(gg)
            vars_t.append((gg, t, b, l, r))
        variants[tid] = vars_t

    top_map = defaultdict(set)
    left_map = defaultdict(set)
    all_vars = set()
    for tid, vs in variants.items():
        for vid, (_, t, _, l, _) in enumerate(vs):
            top_map[t].add((tid, vid))
            left_map[l].add((tid, vid))
            all_vars.add((tid, vid))

    placed = [[None for _ in range(N)] for _ in range(N)]
    used = set()

    def border_ok(r, c, t, b, l, rr):
        if r == 0 and edge_count[canon(t)] != 1:
            return False
        if c == 0 and edge_count[canon(l)] != 1:
            return False
        if r == N - 1 and edge_count[canon(b)] != 1:
            return False
        if c == N - 1 and edge_count[canon(rr)] != 1:
            return False
        return True

    def backtrack(pos):
        if pos == N * N:
            return True
        r = pos // N
        c = pos % N
        need_top = None
        need_left = None
        if r > 0:
            need_top = placed[r - 1][c][2]
        if c > 0:
            need_left = placed[r][c - 1][4]

        if need_top is not None and need_left is not None:
            cand = top_map[need_top] & left_map[need_left]
        elif need_top is not None:
            cand = top_map[need_top]
        elif need_left is not None:
            cand = left_map[need_left]
        else:
            cand = all_vars

        if r == 0 and c == 0:
            cand = [cv for cv in cand if cv[0] in corners]

        for tid, vid in list(cand):
            if tid in used:
                continue
            gg, t, b, l, rr = variants[tid][vid]
            if not border_ok(r, c, t, b, l, rr):
                continue
            used.add(tid)
            placed[r][c] = (tid, gg, b, t, rr, l)
            if backtrack(pos + 1):
                return True
            placed[r][c] = None
            used.remove(tid)
        return False

    ok = backtrack(0)
    if not ok:
        print(part1)
        print(0)
        return

    tile_inner = 8
    image = []
    for r in range(N):
        rows = ['' for _ in range(tile_inner)]
        for c in range(N):
            _, gg, _, _, _, _ = placed[r][c]
            inner = [row[1:-1] for row in gg[1:-1]]
            for k in range(tile_inner):
                rows[k] += inner[k]
        image.extend(rows)

    monster = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ]
    m_pts = [(x, y) for y, row in enumerate(monster) for x, ch in enumerate(row) if ch == '#']
    mh = len(monster)
    mw = len(monster[0])

    def count_monsters(img):
        H = len(img)
        W = len(img[0])
        cnt = 0
        for y in range(H - mh + 1):
            for x in range(W - mw + 1):
                if all(img[y + dy][x + dx] == '#' for dx, dy in m_pts):
                    cnt += 1
        return cnt

    total_hash = sum(row.count('#') for row in image)
    part2 = 0
    for img in orientations(image):
        cnt = count_monsters(img)
        if cnt:
            part2 = total_hash - cnt * len(m_pts)
            break

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
