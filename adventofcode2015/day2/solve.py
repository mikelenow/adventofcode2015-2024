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

    # Day 2: I Was Told There Would Be No Math
    # Part 1: Calculate wrapping paper (2*l*w + 2*w*h + 2*h*l + smallest side)
    # Part 2: Calculate ribbon (perimeter of smallest side + bow = l*w*h)

    total_paper = 0
    total_ribbon = 0

    for line in lines:
        dimensions = list(map(int, line.split('x')))
        l, w, h = sorted(dimensions)

        # Part 1: Surface area + smallest side
        surface_area = 2*l*w + 2*w*h + 2*h*l
        slack = l*w
        total_paper += surface_area + slack

        # Part 2: Smallest perimeter + bow
        smallest_perimeter = 2*l + 2*w
        bow = l*w*h
        total_ribbon += smallest_perimeter + bow

    print(f"Part 1: {total_paper}")
    print(f"Part 2: {total_ribbon}")

if __name__ == '__main__':
    solve()
