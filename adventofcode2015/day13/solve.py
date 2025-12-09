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

    # Day 13: Knights of the Dinner Table
    # Find optimal seating arrangement for happiness

    from itertools import permutations
    import re

    happiness = {}
    people = set()

    for line in lines:
        match = re.match(r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).', line)
        if match:
            person1 = match.group(1)
            sign = 1 if match.group(2) == 'gain' else -1
            amount = int(match.group(3)) * sign
            person2 = match.group(4)
            people.add(person1)
            people.add(person2)
            happiness[(person1, person2)] = amount

    def calculate_happiness(arrangement):
        total = 0
        n = len(arrangement)
        for i in range(n):
            person = arrangement[i]
            left = arrangement[(i - 1) % n]
            right = arrangement[(i + 1) % n]
            total += happiness.get((person, left), 0)
            total += happiness.get((person, right), 0)
        return total

    # Part 1: Find best arrangement
    max_happiness = max(calculate_happiness(perm) for perm in permutations(people))
    part1 = max_happiness

    # Part 2: Add yourself (neutral happiness)
    for person in list(people):
        happiness[('Me', person)] = 0
        happiness[(person, 'Me')] = 0
    people.add('Me')

    max_happiness = max(calculate_happiness(perm) for perm in permutations(people))
    part2 = max_happiness

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
