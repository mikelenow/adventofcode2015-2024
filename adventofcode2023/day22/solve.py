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
    bricks = []
    for line in lines:
        if not line:
            continue
        a, b = line.split('~')
        x1, y1, z1 = (int(v) for v in a.split(','))
        x2, y2, z2 = (int(v) for v in b.split(','))
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if z1 > z2:
            z1, z2 = z2, z1
        bricks.append([x1, y1, z1, x2, y2, z2])

    bricks.sort(key=lambda t: t[2])
    n = len(bricks)

    surface = {}  # (x,y) -> (top_z, brick_id)
    supports = [set() for _ in range(n)]
    supported_by = [set() for _ in range(n)]

    for i, (x1, y1, z1, x2, y2, z2) in enumerate(bricks):
        max_top = 0
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                top, _bid = surface.get((x, y), (0, -1))
                if top > max_top:
                    max_top = top

        below = set()
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                top, bid = surface.get((x, y), (0, -1))
                if top == max_top and bid != -1:
                    below.add(bid)

        dz = z1 - (max_top + 1)
        z1 -= dz
        z2 -= dz
        bricks[i] = [x1, y1, z1, x2, y2, z2]

        supports[i] = below
        for b in below:
            supported_by[b].add(i)

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                surface[(x, y)] = (z2, i)

    part1 = 0
    for i in range(n):
        ok = True
        for up in supported_by[i]:
            if len(supports[up]) == 1:
                ok = False
                break
        if ok:
            part1 += 1

    part2 = 0
    for i in range(n):
        removed = {i}
        stack = [i]
        while stack:
            b = stack.pop()
            for up in supported_by[b]:
                if up in removed:
                    continue
                if supports[up].issubset(removed):
                    removed.add(up)
                    stack.append(up)
        part2 += len(removed) - 1

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
