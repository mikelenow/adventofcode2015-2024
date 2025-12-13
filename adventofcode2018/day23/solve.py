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

    bots = []
    for line in lines:
        if not line:
            continue
        # pos=<x,y,z>, r=r
        left, right = line.split('>,')
        coords = left.split('<')[1]
        x_str, y_str, z_str = coords.split(',')
        r = int(right.split('=')[1])
        bots.append((int(x_str), int(y_str), int(z_str), r))

    if not bots:
        print(0)
        print(0)
        return

    # Part 1
    strongest = max(bots, key=lambda b: b[3])
    sx, sy, sz, sr = strongest
    part1 = 0
    for x, y, z, r in bots:
        if abs(x - sx) + abs(y - sy) + abs(z - sz) <= sr:
            part1 += 1

    # Part 2: cube subdivision with priority queue
    import heapq

    xs = [b[0] for b in bots]
    ys = [b[1] for b in bots]
    zs = [b[2] for b in bots]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)

    def pow2_cover(lo, hi):
        size = 1
        while size < (hi - lo + 1):
            size *= 2
        return size

    size = max(pow2_cover(min_x, max_x), pow2_cover(min_y, max_y), pow2_cover(min_z, max_z))
    # Use the true minimum corner as origin so the cube covers the full bounding box.
    ox, oy, oz = min_x, min_y, min_z

    def dist_point_to_cube(px, py, pz, cube):
        x, y, z, s = cube
        dx = 0
        if px < x:
            dx = x - px
        elif px > x + s - 1:
            dx = px - (x + s - 1)
        dy = 0
        if py < y:
            dy = y - py
        elif py > y + s - 1:
            dy = py - (y + s - 1)
        dz = 0
        if pz < z:
            dz = z - pz
        elif pz > z + s - 1:
            dz = pz - (z + s - 1)
        return dx + dy + dz

    def bots_in_range(cube):
        cnt = 0
        for bx, by, bz, br in bots:
            if dist_point_to_cube(bx, by, bz, cube) <= br:
                cnt += 1
        return cnt

    def dist_origin_to_cube(cube):
        return dist_point_to_cube(0, 0, 0, cube)

    start_cube = (ox, oy, oz, size)
    start_cnt = bots_in_range(start_cube)
    pq = []
    # max cnt, then min dist, then min size
    heapq.heappush(pq, (-start_cnt, dist_origin_to_cube(start_cube), size, start_cube))

    best_dist = None
    while pq:
        neg_cnt, d0, s, cube = heapq.heappop(pq)
        cnt = -neg_cnt
        x, y, z, s = cube

        if s == 1:
            # single point
            if best_dist is None or d0 < best_dist:
                best_dist = d0
            # Since pq is ordered by (-cnt, dist, size), first point popped is optimal
            print(part1)
            print(d0)
            return

        hs = s // 2
        children = [
            (x, y, z, hs),
            (x + hs, y, z, hs),
            (x, y + hs, z, hs),
            (x, y, z + hs, hs),
            (x + hs, y + hs, z, hs),
            (x + hs, y, z + hs, hs),
            (x, y + hs, z + hs, hs),
            (x + hs, y + hs, z + hs, hs),
        ]
        for child in children:
            c_cnt = bots_in_range(child)
            if c_cnt == 0:
                continue
            heapq.heappush(pq, (-c_cnt, dist_origin_to_cube(child), child[3], child))

    print(part1)
    print(best_dist if best_dist is not None else 0)

if __name__ == '__main__':
    solve()
