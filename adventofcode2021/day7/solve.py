import sys
import math

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
    first = ''
    for s in lines:
        if s:
            first = s
            break
    if not first:
        print(0)
        print(0)
        return

    pos = [int(x) for x in first.split(',') if x]
    pos.sort()
    n = len(pos)

    med = pos[n // 2]
    part1 = sum(abs(x - med) for x in pos)

    mean = sum(pos) / n
    cands = {math.floor(mean), math.ceil(mean)}

    def tri(d):
        return d * (d + 1) // 2

    best = None
    for t in cands:
        cost = sum(tri(abs(x - t)) for x in pos)
        if best is None or cost < best:
            best = cost
    part2 = best or 0

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
