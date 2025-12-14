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
    instrs = []
    for line in lines:
        if not line:
            continue
        d, n, color = line.split()
        instrs.append((d, int(n), color.strip('()')))

    dirs = {'R': (1, 0), 'D': (0, 1), 'L': (-1, 0), 'U': (0, -1)}
    dir_from_hex = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}

    def lagoon(steps):
        x = y = 0
        pts = [(0, 0)]
        boundary = 0
        for d, n in steps:
            dx, dy = dirs[d]
            x += dx * n
            y += dy * n
            pts.append((x, y))
            boundary += n

        twice_area = 0
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            twice_area += x1 * y2 - x2 * y1
        twice_area = abs(twice_area)
        return (twice_area + boundary) // 2 + 1

    part1_steps = [(d, n) for (d, n, _) in instrs]
    part1 = lagoon(part1_steps)

    part2_steps = []
    for _, __, color in instrs:
        # #70c710 -> len=0x70c71, dir=0
        n = int(color[1:6], 16)
        d = dir_from_hex[color[6]]
        part2_steps.append((d, n))
    part2 = lagoon(part2_steps)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
