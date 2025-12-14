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
    cubes = set()
    for s in lines:
        if not s:
            continue
        x, y, z = map(int, s.split(','))
        cubes.add((x, y, z))
    if not cubes:
        print(0)
        print(0)
        return

    dirs = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    part1 = 0
    for x, y, z in cubes:
        s = 6
        for dx, dy, dz in dirs:
            if (x + dx, y + dy, z + dz) in cubes:
                s -= 1
        part1 += s

    xs = [x for x, _, _ in cubes]
    ys = [y for _, y, _ in cubes]
    zs = [z for _, _, z in cubes]
    minx, maxx = min(xs) - 1, max(xs) + 1
    miny, maxy = min(ys) - 1, max(ys) + 1
    minz, maxz = min(zs) - 1, max(zs) + 1

    from collections import deque

    start = (minx, miny, minz)
    seen = {start}
    dq = deque([start])
    ext = 0
    while dq:
        x, y, z = dq.popleft()
        for dx, dy, dz in dirs:
            nx, ny, nz = x + dx, y + dy, z + dz
            if nx < minx or nx > maxx or ny < miny or ny > maxy or nz < minz or nz > maxz:
                continue
            np = (nx, ny, nz)
            if np in cubes:
                ext += 1
                continue
            if np in seen:
                continue
            seen.add(np)
            dq.append(np)

    print(part1)
    print(ext)

if __name__ == '__main__':
    solve()
