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

    # Day 6: Probably a Fire Hazard
    # Part 1: Count lights that are on after following instructions (on/off/toggle)
    # Part 2: Sum brightness levels (on=+1, off=-1 min 0, toggle=+2)

    import re

    grid1 = [[False] * 1000 for _ in range(1000)]
    grid2 = [[0] * 1000 for _ in range(1000)]

    for line in lines:
        match = re.match(r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)', line)
        if match:
            action = match.group(1)
            x1, y1, x2, y2 = map(int, match.groups()[1:])

            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    # Part 1
                    if action == 'turn on':
                        grid1[x][y] = True
                    elif action == 'turn off':
                        grid1[x][y] = False
                    else:  # toggle
                        grid1[x][y] = not grid1[x][y]

                    # Part 2
                    if action == 'turn on':
                        grid2[x][y] += 1
                    elif action == 'turn off':
                        grid2[x][y] = max(0, grid2[x][y] - 1)
                    else:  # toggle
                        grid2[x][y] += 2

    part1 = sum(sum(row) for row in grid1)
    part2 = sum(sum(row) for row in grid2)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
