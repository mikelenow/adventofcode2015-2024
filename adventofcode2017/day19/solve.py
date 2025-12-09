import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            # Preserve spaces for the ASCII diagram
            lines = [line.rstrip('\n') for line in f.readlines()]
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    # TODO: Implement solution
    if not lines:
        print("Part 1: ")
        print("Part 2: 0")
        return

    width = max(len(line) for line in lines)
    grid = [line.ljust(width) for line in lines]

    # Find starting position (first '|' in top row)
    row = 0
    col = grid[0].index('|')
    dr, dc = 1, 0  # moving down initially

    letters = []
    steps = 0

    while 0 <= row < len(grid) and 0 <= col < width and grid[row][col] != ' ':
        ch = grid[row][col]
        steps += 1

        if ch.isalpha():
            letters.append(ch)

        if ch == '+':
            # turn: find new direction
            if dr == 0:  # was moving horizontally, try up/down
                if row > 0 and grid[row - 1][col] != ' ':
                    dr, dc = -1, 0
                elif row + 1 < len(grid) and grid[row + 1][col] != ' ':
                    dr, dc = 1, 0
            else:  # was moving vertically, try left/right
                if col > 0 and grid[row][col - 1] != ' ':
                    dr, dc = 0, -1
                elif col + 1 < width and grid[row][col + 1] != ' ':
                    dr, dc = 0, 1

        row += dr
        col += dc

    part1 = ''.join(letters)
    part2 = steps

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
