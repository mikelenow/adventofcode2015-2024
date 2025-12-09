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

    # Day 16: Aunt Sue
    import re

    target = {
        'children': 3, 'cats': 7, 'samoyeds': 2, 'pomeranians': 3,
        'akitas': 0, 'vizslas': 0, 'goldfish': 5, 'trees': 3,
        'cars': 2, 'perfumes': 1
    }

    sues = []
    for line in lines:
        match = re.match(r'Sue (\d+): (.+)', line)
        if match:
            sue_num = int(match.group(1))
            properties = {}
            for prop in match.group(2).split(', '):
                key, val = prop.split(': ')
                properties[key] = int(val)
            sues.append((sue_num, properties))

    # Part 1: Exact match
    for sue_num, props in sues:
        if all(target[key] == val for key, val in props.items()):
            part1 = sue_num
            break

    # Part 2: Ranges for cats, trees, pomeranians, goldfish
    for sue_num, props in sues:
        match = True
        for key, val in props.items():
            if key in ['cats', 'trees']:
                if val <= target[key]:
                    match = False
            elif key in ['pomeranians', 'goldfish']:
                if val >= target[key]:
                    match = False
            else:
                if val != target[key]:
                    match = False
        if match:
            part2 = sue_num
            break

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
