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
    s = ''
    for ln in lines:
        if ln:
            s = ln.strip()
            break
    if not s:
        print(0)
        print(0)
        return

    m = re.match(r'^target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)$', s)
    if not m:
        print(0)
        print(0)
        return
    x1, x2, y1, y2 = map(int, m.groups())
    xmin, xmax = (x1, x2) if x1 <= x2 else (x2, x1)
    ymin, ymax = (y1, y2) if y1 <= y2 else (y2, y1)

    if ymin < 0:
        vy0 = -ymin - 1
        part1 = vy0 * (vy0 + 1) // 2
    else:
        part1 = ymax * (ymax + 1) // 2

    def hits(vx0, vy0):
        x = 0
        y = 0
        vx = vx0
        vy = vy0
        while x <= xmax and y >= ymin:
            x += vx
            y += vy
            if xmin <= x <= xmax and ymin <= y <= ymax:
                return True
            if vx > 0:
                vx -= 1
            elif vx < 0:
                vx += 1
            vy -= 1
        return False

    count = 0
    vx_min = 0
    while vx_min * (vx_min + 1) // 2 < xmin and vx_min <= xmax:
        vx_min += 1
    vx_lo = vx_min
    vx_hi = xmax
    vy_lo = ymin
    vy_hi = (-ymin - 1) if ymin < 0 else ymax
    for vx0 in range(vx_lo, vx_hi + 1):
        for vy0 in range(vy_lo, vy_hi + 1):
            if hits(vx0, vy0):
                count += 1

    print(part1)
    print(count)

if __name__ == '__main__':
    solve()
