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
    grid = lines
    H = len(grid)
    W = len(grid[0]) if H else 0

    sx = sy = None
    for y in range(H):
        x = grid[y].find('S')
        if x != -1:
            sx, sy = x, y
            break
    if sx is None:
        print(0)
        print(0)
        return

    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    pipe = {
        '|': {(0, -1), (0, 1)},
        '-': {(-1, 0), (1, 0)},
        'L': {(0, -1), (1, 0)},
        'J': {(0, -1), (-1, 0)},
        '7': {(0, 1), (-1, 0)},
        'F': {(0, 1), (1, 0)},
    }

    def inb(x, y):
        return 0 <= x < W and 0 <= y < H

    def connects(ch, dx, dy):
        if ch == 'S':
            return True
        return ch in pipe and (dx, dy) in pipe[ch]

    s_conns = []
    for dx, dy in dirs:
        nx, ny = sx + dx, sy + dy
        if not inb(nx, ny):
            continue
        ch = grid[ny][nx]
        if ch in pipe and (-dx, -dy) in pipe[ch]:
            s_conns.append((dx, dy))

    def start_char(conns):
        a, b = sorted(conns)
        if a == (0, -1) and b == (0, 1):
            return '|'
        if a == (-1, 0) and b == (1, 0):
            return '-'
        if a == (0, -1) and b == (1, 0):
            return 'L'
        if a == (-1, 0) and b == (0, -1):
            return 'J'
        if a == (-1, 0) and b == (0, 1):
            return '7'
        return 'F'

    s_as = start_char(s_conns)

    loop = set()
    loop.add((sx, sy))

    px, py = sx, sy
    dx0, dy0 = s_conns[0]
    cx, cy = sx + dx0, sy + dy0
    prev = (sx, sy)
    while (cx, cy) != (sx, sy):
        loop.add((cx, cy))
        ch = grid[cy][cx]
        conns = pipe[ch]
        for ndx, ndy in conns:
            nx, ny = cx + ndx, cy + ndy
            if (nx, ny) != prev:
                prev = (cx, cy)
                cx, cy = nx, ny
                break

    loop_len = len(loop)
    part1 = loop_len // 2

    def loop_char(x, y):
        ch = grid[y][x]
        if ch == 'S':
            return s_as
        return ch

    part2 = 0
    for y in range(H):
        inside = False
        pending = None
        for x in range(W):
            if (x, y) in loop:
                ch = loop_char(x, y)
                if ch == '|':
                    inside = not inside
                elif ch in ('F', 'L'):
                    pending = ch
                elif ch == 'J':
                    if pending == 'F':
                        inside = not inside
                    pending = None
                elif ch == '7':
                    if pending == 'L':
                        inside = not inside
                    pending = None
                continue
            if inside:
                part2 += 1

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
