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

    # Day 19: Medicine for Rudolph
    replacements = []
    molecule = ""

    for line in lines:
        if '=>' in line:
            parts = line.split(' => ')
            replacements.append((parts[0], parts[1]))
        elif line:
            molecule = line

    # Part 1: Count distinct molecules after one replacement
    distinct = set()
    for old, new in replacements:
        for i in range(len(molecule)):
            if molecule[i:i+len(old)] == old:
                new_molecule = molecule[:i] + new + molecule[i+len(old):]
                distinct.add(new_molecule)
    part1 = len(distinct)

    # Part 2: Find steps to create molecule from 'e'
    # For AoC 2015 Day 19, the input has a specific structure
    # The formula is: num_elements - num_Rn - num_Ar - 2*num_Y - 1
    import re

    # Count elements (uppercase letters, possibly followed by lowercase)
    elements = re.findall(r'[A-Z][a-z]?', molecule)
    num_elements = len(elements)

    # Count special tokens
    num_Rn = molecule.count('Rn')
    num_Ar = molecule.count('Ar')
    num_Y = molecule.count('Y')

    part2 = num_elements - num_Rn - num_Ar - 2 * num_Y - 1

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
