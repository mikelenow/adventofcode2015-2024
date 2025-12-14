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
    pat = re.compile(r"x=(-?\d+), y=(-?\d+)")
    sensors = []
    beacons = set()
    max_abs = 0
    for s in lines:
        if not s:
            continue
        nums = pat.findall(s)
        if len(nums) != 2:
            continue
        sx, sy = map(int, nums[0])
        bx, by = map(int, nums[1])
        d = abs(sx - bx) + abs(sy - by)
        sensors.append((sx, sy, d))
        beacons.add((bx, by))
        max_abs = max(max_abs, abs(sx), abs(sy), abs(bx), abs(by))

    if not sensors:
        print(0)
        print(0)
        return

    if max_abs <= 1000:
        target_y = 10
        limit = 20
    else:
        target_y = 2000000
        limit = 4000000

    intervals = []
    for sx, sy, d in sensors:
        dy = abs(sy - target_y)
        if dy > d:
            continue
        rem = d - dy
        intervals.append((sx - rem, sx + rem))
    intervals.sort()

    merged = []
    for a, b in intervals:
        if not merged or a > merged[-1][1] + 1:
            merged.append([a, b])
        else:
            if b > merged[-1][1]:
                merged[-1][1] = b

    covered = 0
    for a, b in merged:
        covered += b - a + 1

    for bx, by in beacons:
        if by != target_y:
            continue
        for a, b in merged:
            if a <= bx <= b:
                covered -= 1
                break

    part1 = covered

    pos = set()
    neg = set()
    for sx, sy, d in sensors:
        r = d + 1
        pos.add(sx + sy + r)
        pos.add(sx + sy - r)
        neg.add(sx - sy + r)
        neg.add(sx - sy - r)

    candidates = []
    for a in pos:
        for b in neg:
            if (a + b) % 2 != 0:
                continue
            x = (a + b) // 2
            y = (a - b) // 2
            if 0 <= x <= limit and 0 <= y <= limit:
                candidates.append((x, y))

    def ok(x, y):
        for sx, sy, d in sensors:
            if abs(sx - x) + abs(sy - y) <= d:
                return False
        return True

    part2 = 0
    seen = set()
    for x, y in candidates:
        if (x, y) in seen:
            continue
        seen.add((x, y))
        if ok(x, y):
            part2 = x * 4000000 + y
            break

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
