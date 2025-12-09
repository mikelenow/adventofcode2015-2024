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

    # Day 25: Let It Snow
    import re

    match = re.search(r'row (\d+), column (\d+)', lines[0])
    target_row = int(match.group(1))
    target_col = int(match.group(2))

    # Calculate position in diagonal sequence
    # Position in diagonal d (1-indexed): sum of 1 to d-1 + position in diagonal
    # Row r, col c is in diagonal (r+c-1), at position c in that diagonal
    diagonal = target_row + target_col - 1
    position_in_sequence = (diagonal * (diagonal - 1)) // 2 + target_col

    # Generate code at that position
    code = 20151125
    for _ in range(position_in_sequence - 1):
        code = (code * 252533) % 33554393

    part1 = code
    part2 = "Merry Christmas!"

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
