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

    keypad1 = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9']
    ]

    keypad2 = [
        [None, None, '1', None, None],
        [None, '2', '3', '4', None],
        ['5', '6', '7', '8', '9'],
        [None, 'A', 'B', 'C', None],
        [None, None, 'D', None, None]
    ]

    def get_code(keypad, start_r, start_c):
        r, c = start_r, start_c
        code = ""
        for line in lines:
            for move in line:
                nr, nc = r, c
                if move == 'U':
                    nr = r - 1
                elif move == 'D':
                    nr = r + 1
                elif move == 'L':
                    nc = c - 1
                elif move == 'R':
                    nc = c + 1

                if 0 <= nr < len(keypad) and 0 <= nc < len(keypad[0]) and keypad[nr][nc] is not None:
                    r, c = nr, nc

            code += keypad[r][c]
        return code

    part1 = get_code(keypad1, 1, 1)
    part2 = get_code(keypad2, 2, 0)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
