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

    # Day 17: No Such Thing as Too Much
    from itertools import combinations

    containers = [int(line) for line in lines]
    target = 150

    # Part 1: Count all combinations that sum to target
    valid_combinations = []
    for r in range(1, len(containers) + 1):
        for combo in combinations(containers, r):
            if sum(combo) == target:
                valid_combinations.append(combo)

    part1 = len(valid_combinations)

    # Part 2: Count combinations using minimum number of containers
    min_containers = min(len(combo) for combo in valid_combinations)
    part2 = sum(1 for combo in valid_combinations if len(combo) == min_containers)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
