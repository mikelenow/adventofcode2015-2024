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

    import re

    discs = []
    for line in lines:
        if line:
            match = re.match(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).', line)
            if match:
                disc_num, positions, start_pos = map(int, match.groups())
                discs.append((positions, start_pos))

    def find_time(discs):
        t = 0
        while True:
            success = True
            for i, (positions, start_pos) in enumerate(discs):
                if (start_pos + t + i + 1) % positions != 0:
                    success = False
                    break
            if success:
                return t
            t += 1

    part1 = find_time(discs)

    # Part 2: Add disc #7 with 11 positions at position 0
    discs_part2 = discs + [(11, 0)]
    part2 = find_time(discs_part2)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
