import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            lines = [line.rstrip('\n\r') for line in f.readlines()]
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    # TODO: Implement solution
    i = 0
    board_lines = []
    while i < len(lines) and lines[i] != '':
        board_lines.append(lines[i])
        i += 1
    while i < len(lines) and lines[i] == '':
        i += 1
    path = lines[i] if i < len(lines) else ''

    if not board_lines:
        print(0)
        print(0)
        return

    W = max(len(r) for r in board_lines)
    H = len(board_lines)
    grid = [r.ljust(W, ' ') for r in board_lines]

    import re
    tokens = re.findall(r"\d+|[LR]", path)

    start_x = None
    for x, ch in enumerate(grid[0]):
        if ch == '.':
            start_x = x
            break
    if start_x is None:
        print(0)
        print(0)
        return

    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    row_rng = []
    for y in range(H):
        xs = [x for x in range(W) if grid[y][x] != ' ']
        if xs:
            row_rng.append((min(xs), max(xs)))
        else:
            row_rng.append((0, -1))
    col_rng = []
    for x in range(W):
        ys = [y for y in range(H) if grid[y][x] != ' ']
        if ys:
            col_rng.append((min(ys), max(ys)))
        else:
            col_rng.append((0, -1))

    def walk(wrap):
        x = start_x
        y = 0
        d = 0
        for t in tokens:
            if t == 'L':
                d = (d - 1) % 4
                continue
            if t == 'R':
                d = (d + 1) % 4
                continue
            n = int(t)
            for _ in range(n):
                dx, dy = dirs[d]
                nx = x + dx
                ny = y + dy
                nd = d
                if not (0 <= nx < W and 0 <= ny < H) or grid[ny][nx] == ' ':
                    nx, ny, nd = wrap(x, y, d)
                if grid[ny][nx] == '#':
                    break
                x, y, d = nx, ny, nd
        return x, y, d

    def wrap_flat(x, y, d):
        if d == 0:
            a, b = row_rng[y]
            return a, y, d
        if d == 2:
            a, b = row_rng[y]
            return b, y, d
        if d == 1:
            a, b = col_rng[x]
            return x, a, d
        a, b = col_rng[x]
        return x, b, d

    x1, y1, d1 = walk(wrap_flat)
    part1 = 1000 * (y1 + 1) + 4 * (x1 + 1) + d1

    runs = []
    for y in range(H):
        x = 0
        while x < W:
            if grid[y][x] == ' ':
                x += 1
                continue
            s = x
            while x < W and grid[y][x] != ' ':
                x += 1
            runs.append(x - s)
    N = min(runs) if runs else 0
    if N == 0:
        print(part1)
        print(0)
        return

    faces = {}
    face_by_block = {}
    fid = 0
    for by in range((H + N - 1) // N):
        for bx in range((W + N - 1) // N):
            gx = bx * N
            gy = by * N
            if gy >= H or gx >= W:
                continue
            if grid[gy][gx] == ' ':
                continue
            face_by_block[(bx, by)] = fid
            faces[fid] = {'bx': bx, 'by': by}
            fid += 1

    sx_block = start_x // N
    sy_block = 0
    start_face = face_by_block[(sx_block, sy_block)]

    def vadd(a, b):
        return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

    def vmul(a, k):
        return (a[0] * k, a[1] * k, a[2] * k)

    def vneg(a):
        return (-a[0], -a[1], -a[2])

    def rot_neighbor(u, v, n, dir2d):
        if dir2d == 0:
            return (vneg(n), v, u)
        if dir2d == 2:
            return (n, v, vneg(u))
        if dir2d == 1:
            return (u, vneg(n), v)
        return (u, n, vneg(v))

    from collections import deque
    orient = {}
    origin = {}
    orient[start_face] = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    origin[start_face] = (0, 0, 0)
    dq = deque([start_face])
    while dq:
        f = dq.popleft()
        bx = faces[f]['bx']
        by = faces[f]['by']
        u, v, n = orient[f]
        o = origin[f]
        for d2, (dbx, dby) in enumerate([(1, 0), (0, 1), (-1, 0), (0, -1)]):
            nb = (bx + dbx, by + dby)
            if nb not in face_by_block:
                continue
            g = face_by_block[nb]
            if g in orient:
                continue
            nu, nv, nn = rot_neighbor(u, v, n, d2)
            if d2 == 0:
                no = vadd(o, vmul(u, N))
            elif d2 == 1:
                no = vadd(o, vmul(v, N))
            elif d2 == 2:
                no = vadd(o, vmul(vneg(nu), N))
            else:
                no = vadd(o, vmul(vneg(nv), N))
            orient[g] = (nu, nv, nn)
            origin[g] = no
            dq.append(g)

    def corners(f):
        u, v, _ = orient[f]
        o = origin[f]
        p00 = o
        p10 = vadd(o, vmul(u, N))
        p01 = vadd(o, vmul(v, N))
        p11 = vadd(p10, vmul(v, N))
        return p00, p10, p01, p11

    def edge_info(f, d):
        p00, p10, p01, p11 = corners(f)
        u, v, _ = orient[f]
        if d == 0:
            return (p10, p11)
        if d == 2:
            return (p00, p01)
        if d == 3:
            return (p00, p10)
        return (p01, p11)

    def canon(a, b):
        return (a, b) if a <= b else (b, a)

    edge_map = {}
    for f in faces:
        for d in range(4):
            a, b = edge_info(f, d)
            edge_map.setdefault(canon(a, b), []).append((f, d, a, b))

    trans = {}
    for k, items in edge_map.items():
        if len(items) != 2:
            continue
        (f1, d1e, a1, b1), (f2, d2e, a2, b2) = items
        trans[(f1, d1e)] = (f2, d2e, (a1 == a2 and b1 == b2))
        trans[(f2, d2e)] = (f1, d1e, (a1 == a2 and b1 == b2))

    def wrap_cube(x, y, d):
        bx = x // N
        by = y // N
        f = face_by_block[(bx, by)]
        lx = x % N
        ly = y % N
        g, edge_d, same = trans[(f, d)]
        t = ly if d in (0, 2) else lx
        t2 = t if same else (N - 1 - t)
        if edge_d == 0:
            nlx, nly = N - 1, t2
        elif edge_d == 2:
            nlx, nly = 0, t2
        elif edge_d == 1:
            nlx, nly = t2, N - 1
        else:
            nlx, nly = t2, 0
        nd = (edge_d + 2) % 4
        nx = faces[g]['bx'] * N + nlx
        ny = faces[g]['by'] * N + nly
        return nx, ny, nd

    x2, y2, d2 = walk(wrap_cube)
    part2 = 1000 * (y2 + 1) + 4 * (x2 + 1) + d2

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
