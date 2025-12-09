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
    layers = {}
    for line in lines:
        if not line:
            continue
        depth_s, range_s = line.split(':')
        d = int(depth_s.strip())
        r = int(range_s.strip())
        layers[d] = r

    def severity(delay):
        total = 0
        for d, r in layers.items():
            period = 2 * (r - 1)
            if (d + delay) % period == 0:
                total += d * r
        return total

    part1 = severity(0)

    delay = 0
    while True:
        caught = False
        for d, r in layers.items():
            period = 2 * (r - 1)
            if (d + delay) % period == 0:
                caught = True
                break
        if not caught:
            part2 = delay
            break
        delay += 1

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
