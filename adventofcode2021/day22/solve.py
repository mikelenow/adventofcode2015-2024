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
    pat = re.compile(r'^(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)$')
    steps = []
    for s in lines:
        if not s:
            continue
        m = pat.match(s)
        if not m:
            continue
        on = (m.group(1) == 'on')
        x1, x2, y1, y2, z1, z2 = map(int, m.groups()[1:])
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if z1 > z2:
            z1, z2 = z2, z1
        steps.append((on, (x1, x2, y1, y2, z1, z2)))

    if not steps:
        print(0)
        print(0)
        return

    on_set = set()
    for on, (x1, x2, y1, y2, z1, z2) in steps:
        ix1 = max(x1, -50)
        ix2 = min(x2, 50)
        iy1 = max(y1, -50)
        iy2 = min(y2, 50)
        iz1 = max(z1, -50)
        iz2 = min(z2, 50)
        if ix1 > ix2 or iy1 > iy2 or iz1 > iz2:
            continue
        for x in range(ix1, ix2 + 1):
            for y in range(iy1, iy2 + 1):
                for z in range(iz1, iz2 + 1):
                    p = (x, y, z)
                    if on:
                        on_set.add(p)
                    else:
                        on_set.discard(p)
    part1 = len(on_set)

    def intersect(a, b):
        ax1, ax2, ay1, ay2, az1, az2 = a
        bx1, bx2, by1, by2, bz1, bz2 = b
        x1 = max(ax1, bx1)
        x2 = min(ax2, bx2)
        y1 = max(ay1, by1)
        y2 = min(ay2, by2)
        z1 = max(az1, bz1)
        z2 = min(az2, bz2)
        if x1 > x2 or y1 > y2 or z1 > z2:
            return None
        return (x1, x2, y1, y2, z1, z2)

    def volume(c):
        x1, x2, y1, y2, z1, z2 = c
        return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)

    acc = []
    for on, cub in steps:
        adds = []
        for sign, c in acc:
            inter = intersect(c, cub)
            if inter is not None:
                adds.append((-sign, inter))
        if on:
            adds.append((1, cub))
        acc.extend(adds)

    total = 0
    for sign, c in acc:
        total += sign * volume(c)
    part2 = total

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
