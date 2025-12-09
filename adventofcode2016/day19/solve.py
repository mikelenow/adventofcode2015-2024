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

    num_elves = int(lines[0])

    # Part 1: Josephus problem
    def josephus(n):
        p = 1
        while p * 2 <= n:
            p *= 2
        return 2 * (n - p) + 1

    part1 = josephus(num_elves)

    # Part 2: Opposite elf variant
    def josephus_opposite(n):
        p = 1
        while p * 3 <= n:
            p *= 3
        if n == p:
            return n
        elif n <= 2 * p:
            return n - p
        else:
            return 2 * n - 3 * p

    part2 = josephus_opposite(num_elves)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
