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

    # TODO: Implement solution
    grid = lines
    H = len(grid)
    W = len(grid[0]) if H else 0

    numbers = []
    digit_to_num = {}
    for y in range(H):
        x = 0
        row = grid[y]
        while x < W:
            if not row[x].isdigit():
                x += 1
                continue
            x0 = x
            while x < W and row[x].isdigit():
                x += 1
            val = int(row[x0:x])
            idx = len(numbers)
            numbers.append((val, y, x0, x))
            for xx in range(x0, x):
                digit_to_num[(xx, y)] = idx

    def is_symbol(ch):
        return (not ch.isdigit()) and ch != '.'

    part1 = 0
    for idx, (val, y, x0, x1) in enumerate(numbers):
        found = False
        for yy in range(max(0, y - 1), min(H, y + 2)):
            for xx in range(max(0, x0 - 1), min(W, x1 + 1)):
                if is_symbol(grid[yy][xx]):
                    found = True
                    break
            if found:
                break
        if found:
            part1 += val

    part2 = 0
    for y in range(H):
        for x in range(W):
            if grid[y][x] != '*':
                continue
            adj = set()
            for yy in range(max(0, y - 1), min(H, y + 2)):
                for xx in range(max(0, x - 1), min(W, x + 2)):
                    if (xx, yy) in digit_to_num:
                        adj.add(digit_to_num[(xx, yy)])
            if len(adj) == 2:
                a, b = list(adj)
                part2 += numbers[a][0] * numbers[b][0]

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
