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

    # Day 24: It Hangs in the Balance
    from itertools import combinations
    from functools import reduce
    import operator

    packages = [int(line) for line in lines]

    def find_quantum_entanglement(num_groups):
        target_weight = sum(packages) // num_groups

        # Find smallest group that sums to target
        for group_size in range(1, len(packages)):
            valid_groups = []
            for combo in combinations(packages, group_size):
                if sum(combo) == target_weight:
                    qe = reduce(operator.mul, combo, 1)
                    valid_groups.append(qe)

            if valid_groups:
                return min(valid_groups)

        return None

    part1 = find_quantum_entanglement(3)
    part2 = find_quantum_entanglement(4)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
