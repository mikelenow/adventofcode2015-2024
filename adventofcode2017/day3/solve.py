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
    if not lines or not lines[0]:
        print("Part 1: 0")
        print("Part 2: 0")
        return

    n = int(lines[0])

    # Part 1: Manhattan distance in the spiral
    if n == 1:
        dist1 = 0
    else:
        layer = 0
        while (2 * layer + 1) ** 2 < n:
            layer += 1
        side_len = 2 * layer + 1
        max_val = side_len ** 2
        # Midpoints of each side on this layer
        mids = [max_val - layer - (side_len - 1) * i for i in range(4)]
        dist1 = layer + min(abs(n - m) for m in mids)

    # Part 2: first value written that is larger than n using neighbor sums
    from collections import defaultdict

    values = defaultdict(int)
    x = y = 0
    values[(0, 0)] = 1
    val2 = 0

    # Spiral traversal: right, up, left, down, increasing step sizes
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    step_size = 1

    def neighbor_sum(cx, cy):
        s = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                s += values[(cx + dx, cy + dy)]
        return s

    while True:
        for i, (dx, dy) in enumerate(directions):
            for _ in range(step_size):
                x += dx
                y += dy
                v = neighbor_sum(x, y)
                values[(x, y)] = v
                if v > n:
                    val2 = v
                    break
            if val2:
                break
            # Increase step size after moving in two directions
            if i % 2 == 1:
                step_size += 1
        if val2:
            break

    print(f"Part 1: {dist1}")
    print(f"Part 2: {val2}")

if __name__ == '__main__':
    solve()
