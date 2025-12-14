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
    rocks = set()
    maxy = 0
    for s in lines:
        if not s:
            continue
        pts = []
        for part in s.split('->'):
            x, y = part.strip().split(',')
            x = int(x)
            y = int(y)
            pts.append((x, y))
            if y > maxy:
                maxy = y
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            if x1 == x2:
                if y1 > y2:
                    y1, y2 = y2, y1
                for y in range(y1, y2 + 1):
                    rocks.add((x1, y))
            elif y1 == y2:
                if x1 > x2:
                    x1, x2 = x2, x1
                for x in range(x1, x2 + 1):
                    rocks.add((x, y1))

    src = (500, 0)

    def drop(blocked, floor_y, abyss_stop):
        x, y = src
        while True:
            if abyss_stop and y > maxy:
                return None
            if floor_y is not None and y + 1 == floor_y:
                return (x, y)
            if (x, y + 1) not in blocked:
                y += 1
                continue
            if (x - 1, y + 1) not in blocked:
                x -= 1
                y += 1
                continue
            if (x + 1, y + 1) not in blocked:
                x += 1
                y += 1
                continue
            return (x, y)

    blocked = set(rocks)
    c1 = 0
    while True:
        p = drop(blocked, None, True)
        if p is None:
            break
        blocked.add(p)
        c1 += 1

    floor_y = maxy + 2
    blocked = set(rocks)
    c2 = 0
    while True:
        if src in blocked:
            break
        p = drop(blocked, floor_y, False)
        blocked.add(p)
        c2 += 1

    print(c1)
    print(c2)

if __name__ == '__main__':
    solve()
