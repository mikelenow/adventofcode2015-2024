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
    import re

    pts = []
    for line in lines:
        if not line:
            continue
        m = re.match(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line)
        if not m:
            continue
        pts.append([int(m.group(1)), int(m.group(2)), int(m.group(3))])
    if not pts:
        print(0)
        print(0)
        return

    n = len(pts)
    pos = [p[:] for p in pts]
    vel = [[0, 0, 0] for _ in range(n)]

    for _ in range(1000):
        for i in range(n):
            for j in range(i + 1, n):
                for a in range(3):
                    if pos[i][a] < pos[j][a]:
                        vel[i][a] += 1
                        vel[j][a] -= 1
                    elif pos[i][a] > pos[j][a]:
                        vel[i][a] -= 1
                        vel[j][a] += 1
        for i in range(n):
            for a in range(3):
                pos[i][a] += vel[i][a]

    part1 = 0
    for i in range(n):
        pot = abs(pos[i][0]) + abs(pos[i][1]) + abs(pos[i][2])
        kin = abs(vel[i][0]) + abs(vel[i][1]) + abs(vel[i][2])
        part1 += pot * kin

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)

    def lcm(a, b):
        return a // gcd(a, b) * b

    def axis_period(axis: int) -> int:
        p = [pts[i][axis] for i in range(n)]
        v = [0] * n
        init = (tuple(p), tuple(v))
        steps = 0
        while True:
            for i in range(n):
                for j in range(i + 1, n):
                    if p[i] < p[j]:
                        v[i] += 1
                        v[j] -= 1
                    elif p[i] > p[j]:
                        v[i] -= 1
                        v[j] += 1
            for i in range(n):
                p[i] += v[i]
            steps += 1
            if (tuple(p), tuple(v)) == init:
                return steps

    px = axis_period(0)
    py = axis_period(1)
    pz = axis_period(2)
    part2 = lcm(lcm(px, py), pz)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
