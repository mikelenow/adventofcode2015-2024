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

    serial = None
    for line in lines:
        if line:
            serial = int(line)
            break
    if serial is None:
        print('')
        print('')
        return

    size = 300

    def power(x: int, y: int) -> int:
        rack = x + 10
        p = rack * y
        p += serial
        p *= rack
        digit = (p // 100) % 10
        return digit - 5

    # Summed-area table sat[x][y] for 1..300 (use 0 border)
    sat = [[0] * (size + 1) for _ in range(size + 1)]
    for y in range(1, size + 1):
        row_sum = 0
        for x in range(1, size + 1):
            row_sum += power(x, y)
            sat[y][x] = sat[y - 1][x] + row_sum

    def square_sum(x: int, y: int, k: int) -> int:
        x2 = x + k - 1
        y2 = y + k - 1
        return sat[y2][x2] - sat[y - 1][x2] - sat[y2][x - 1] + sat[y - 1][x - 1]

    best3 = None
    best3_xy = (1, 1)
    k = 3
    for y in range(1, size - k + 2):
        for x in range(1, size - k + 2):
            s = square_sum(x, y, k)
            if best3 is None or s > best3:
                best3 = s
                best3_xy = (x, y)
    part1 = f"{best3_xy[0]},{best3_xy[1]}"

    best = None
    best_xyz = (1, 1, 1)
    # Brute force sizes 1..300 with SAT (fast enough in Python)
    for k in range(1, size + 1):
        limit = size - k + 1
        for y in range(1, limit + 1):
            for x in range(1, limit + 1):
                s = square_sum(x, y, k)
                if best is None or s > best:
                    best = s
                    best_xyz = (x, y, k)
    part2 = f"{best_xyz[0]},{best_xyz[1]},{best_xyz[2]}"

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
