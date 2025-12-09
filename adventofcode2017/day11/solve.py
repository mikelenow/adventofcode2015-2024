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

    steps = [s for s in lines[0].split(',') if s]

    # cube coordinates for hex grid
    moves = {
        'n':  (0, 1, -1),
        's':  (0, -1, 1),
        'ne': (1, 0, -1),
        'sw': (-1, 0, 1),
        'nw': (-1, 1, 0),
        'se': (1, -1, 0),
    }

    x = y = z = 0
    max_dist = 0

    def dist(a, b, c):
        return max(abs(a), abs(b), abs(c))

    for s in steps:
        dx, dy, dz = moves[s]
        x += dx
        y += dy
        z += dz
        max_dist = max(max_dist, dist(x, y, z))

    part1 = dist(x, y, z)
    part2 = max_dist

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
