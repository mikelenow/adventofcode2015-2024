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

    import re

    screen = [[False] * 50 for _ in range(6)]

    for line in lines:
        if line.startswith('rect'):
            match = re.match(r'rect (\d+)x(\d+)', line)
            if match:
                w, h = map(int, match.groups())
                for r in range(h):
                    for c in range(w):
                        screen[r][c] = True

        elif line.startswith('rotate row'):
            match = re.match(r'rotate row y=(\d+) by (\d+)', line)
            if match:
                row, shift = map(int, match.groups())
                screen[row] = screen[row][-shift:] + screen[row][:-shift]

        elif line.startswith('rotate column'):
            match = re.match(r'rotate column x=(\d+) by (\d+)', line)
            if match:
                col, shift = map(int, match.groups())
                column = [screen[r][col] for r in range(6)]
                column = column[-shift:] + column[:-shift]
                for r in range(6):
                    screen[r][col] = column[r]

    lit_pixels = sum(sum(row) for row in screen)
    print(f"Part 1: {lit_pixels}")

    print("Part 2:")
    for row in screen:
        print(''.join('#' if pixel else '.' for pixel in row))

if __name__ == '__main__':
    solve()
