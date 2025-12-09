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

    # Day 1: Not Quite Lisp
    # Part 1: Find final floor
    # Part 2: Find position of first character that causes entering basement (-1)

    data = lines[0]

    # Part 1: Count parentheses
    floor = data.count('(') - data.count(')')

    # Part 2: Find first position entering basement
    current_floor = 0
    basement_pos = None
    for i, char in enumerate(data, 1):
        if char == '(':
            current_floor += 1
        else:
            current_floor -= 1
        if current_floor == -1 and basement_pos is None:
            basement_pos = i
            break

    print(f"Part 1: {floor}")
    print(f"Part 2: {basement_pos}")

if __name__ == '__main__':
    solve()
