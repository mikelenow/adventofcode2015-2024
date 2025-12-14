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

    # Part 2: coarse-to-fine search by step halving.
    min_x = min(x - r for x, _, _, r in bots)
    max_x = max(x + r for x, _, _, r in bots)
    min_y = min(y - r for _, y, _, r in bots)
    max_y = max(y + r for _, y, _, r in bots)
    min_z = min(z - r for _, _, z, r in bots)
    max_z = max(z + r for _, _, z, r in bots)

    def in_range_count(px, py, pz, step):
        cnt = 0
        for bx, by, bz, br in bots:
            # distance from point to bot center in manhattan, but scaled by step using ceil
            d = abs(bx - px) + abs(by - py) + abs(bz - pz)
            if d - br <= 0:
                cnt += 1
        return cnt

    step = 1
    span = max(max_x - min_x, max_y - min_y, max_z - min_z)
    while step < span:
        step *= 2

    best_x = 0
    best_y = 0
    best_z = 0

    while step >= 1:
        best = None  # (negcnt, dist, x,y,z)
        # Search in current bounding box on this grid
        for x in range(min_x, max_x + 1, step):
            for y in range(min_y, max_y + 1, step):
                for z in range(min_z, max_z + 1, step):
                    cnt = 0
                    for bx, by, bz, br in bots:
                        d = abs(bx - x) + abs(by - y) + abs(bz - z)
                        if d <= br + (step - 1) * 3:
                            # conservative: point within step-sized neighborhood might be in range
                            cnt += 1
                    dist0 = abs(x) + abs(y) + abs(z)
                    key = (-cnt, dist0, x, y, z)
                    if best is None or key < best:
                        best = key

        _, _, best_x, best_y, best_z = best

        # Narrow bounds around best point
        min_x = best_x - step
        max_x = best_x + step
        min_y = best_y - step
        max_y = best_y + step
        min_z = best_z - step
        max_z = best_z + step
        step //= 2

    # Final exact count at the best point
    final_cnt = 0
    for bx, by, bz, br in bots:
        if abs(bx - best_x) + abs(by - best_y) + abs(bz - best_z) <= br:
            final_cnt += 1
    part2 = abs(best_x) + abs(best_y) + abs(best_z)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
