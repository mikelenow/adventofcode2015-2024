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
    scanners = []
    cur = []
    for s in lines + ['']:
        if not s:
            if cur:
                scanners.append(cur)
                cur = []
            continue
        if s.startswith('---'):
            continue
        x, y, z = (int(v) for v in s.split(','))
        cur.append((x, y, z))

    if not scanners:
        print(0)
        print(0)
        return

    def rots(p):
        x, y, z = p
        return [
            ( x,  y,  z), ( x, -y, -z), ( x,  z, -y), ( x, -z,  y),
            (-x,  y, -z), (-x, -y,  z), (-x,  z,  y), (-x, -z, -y),
            ( y,  x, -z), ( y, -x,  z), ( y,  z,  x), ( y, -z, -x),
            (-y,  x,  z), (-y, -x, -z), (-y,  z, -x), (-y, -z,  x),
            ( z,  x,  y), ( z, -x, -y), ( z,  y, -x), ( z, -y,  x),
            (-z,  x, -y), (-z, -x,  y), (-z,  y,  x), (-z, -y, -x),
        ]

    rot_scanners = []
    for pts in scanners:
        per_rot = [[] for _ in range(24)]
        for p in pts:
            rp = rots(p)
            for i in range(24):
                per_rot[i].append(rp[i])
        rot_scanners.append(per_rot)

    placed = {0: (0, 0, 0)}
    abs_beacons = set(rot_scanners[0][0])
    abs_beacons_set = abs_beacons
    remaining = set(range(1, len(scanners)))

    def addp(a, b):
        return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

    def subp(a, b):
        return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

    while remaining:
        progress = False
        known_list = list(abs_beacons_set)
        known_set = abs_beacons_set
        for sid in list(remaining):
            matched = False
            for ridx in range(24):
                pts = rot_scanners[sid][ridx]
                counts = {}
                for p in pts:
                    for q in known_list:
                        off = subp(q, p)
                        counts[off] = counts.get(off, 0) + 1
                best_off = None
                for off, c in counts.items():
                    if c >= 12:
                        best_off = off
                        break
                if best_off is None:
                    continue
                placed[sid] = best_off
                for p in pts:
                    abs_beacons.add(addp(p, best_off))
                abs_beacons_set = abs_beacons
                remaining.remove(sid)
                progress = True
                matched = True
                break
            if matched:
                break
        if not progress:
            break

    part1 = len(abs_beacons_set)
    pos = [placed[i] for i in placed]
    part2 = 0
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            a = pos[i]
            b = pos[j]
            d = abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
            if d > part2:
                part2 = d

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
