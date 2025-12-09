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

    step = int(lines[0])

    # Part 1
    buf = [0]
    pos = 0
    for i in range(1, 2018):
        pos = (pos + step) % len(buf) + 1
        buf.insert(pos, i)

    idx = buf.index(2017)
    part1 = buf[(idx + 1) % len(buf)]

    # Part 2: track value after 0 without storing full buffer
    pos = 0
    value_after_zero = 0
    size = 1
    for i in range(1, 50_000_000 + 1):
        pos = (pos + step) % size + 1
        if pos == 1:
            value_after_zero = i
        size += 1

    part2 = value_after_zero

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
