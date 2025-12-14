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
    grid = [line for line in lines if line]
    ast = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == '#':
                ast.append((x, y))
    if not ast:
        print(0)
        print(0)
        return

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)

    best = None
    best_pos = None
    for x0, y0 in ast:
        seen = set()
        for x1, y1 in ast:
            if (x1, y1) == (x0, y0):
                continue
            dx = x1 - x0
            dy = y1 - y0
            g = gcd(abs(dx), abs(dy))
            dx //= g
            dy //= g
            seen.add((dx, dy))
        if best is None or len(seen) > best:
            best = len(seen)
            best_pos = (x0, y0)

    part1 = best

    # Part 2: vaporization order
    import math
    sx, sy = best_pos
    by_dir = {}
    for x, y in ast:
        if (x, y) == (sx, sy):
            continue
        dx = x - sx
        dy = y - sy
        g = gcd(abs(dx), abs(dy))
        ndx = dx // g
        ndy = dy // g
        dist = abs(dx) + abs(dy)
        by_dir.setdefault((ndx, ndy), []).append((dist, x, y))

    for k in by_dir:
        by_dir[k].sort()

    # angle: 0 at up (0,-1), clockwise
    def angle(d):
        dx, dy = d
        return (math.atan2(dx, -dy) + 2 * math.pi) % (2 * math.pi)

    dirs = sorted(by_dir.keys(), key=angle)
    vaporized = []
    while True:
        any_left = False
        for d in dirs:
            lst = by_dir[d]
            if lst:
                any_left = True
                _, x, y = lst.pop(0)
                vaporized.append((x, y))
        if not any_left:
            break

    if len(vaporized) >= 200:
        x200, y200 = vaporized[199]
        part2 = x200 * 100 + y200
    else:
        part2 = 0

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
