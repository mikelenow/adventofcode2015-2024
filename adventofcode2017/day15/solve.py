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
    if len(lines) < 2:
        print("Part 1: 0")
        print("Part 2: 0")
        return

    def parse_start(line):
        # "Generator A starts with 722"
        return int(line.split()[-1])

    start_a = parse_start(lines[0])
    start_b = parse_start(lines[1])

    factor_a = 16807
    factor_b = 48271
    mod = 2147483647

    def gen(start, factor, multiple=1):
        val = start
        while True:
            val = (val * factor) % mod
            if val % multiple == 0:
                yield val

    # Part 1
    ga = gen(start_a, factor_a)
    gb = gen(start_b, factor_b)
    matches = 0
    for _ in range(40_000_000):
        if (next(ga) & 0xFFFF) == (next(gb) & 0xFFFF):
            matches += 1

    part1 = matches

    # Part 2
    ga = gen(start_a, factor_a, 4)
    gb = gen(start_b, factor_b, 8)
    matches = 0
    for _ in range(5_000_000):
        if (next(ga) & 0xFFFF) == (next(gb) & 0xFFFF):
            matches += 1

    part2 = matches

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
