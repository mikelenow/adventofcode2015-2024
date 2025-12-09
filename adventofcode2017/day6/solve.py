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

    banks = [int(x) for x in lines[0].split()]

    seen = {}
    steps = 0

    while True:
        config = tuple(banks)
        if config in seen:
            part1 = steps
            part2 = steps - seen[config]
            break
        seen[config] = steps

        # Find index of the bank with the most blocks (lowest index on ties)
        max_blocks = max(banks)
        idx = banks.index(max_blocks)
        banks[idx] = 0
        i = idx
        while max_blocks > 0:
            i = (i + 1) % len(banks)
            banks[i] += 1
            max_blocks -= 1
        steps += 1

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
