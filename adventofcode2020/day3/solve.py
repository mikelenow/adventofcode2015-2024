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

    grid = [s for s in lines if s]
    if not grid:
        print(0)
        print(0)
        return

    h = len(grid)
    w = len(grid[0])

    def count(dx, dy):
        x = 0
        y = 0
        trees = 0
        while y < h:
            if grid[y][x % w] == '#':
                trees += 1
            x += dx
            y += dy
        return trees

    part1 = count(3, 1)
    prod = 1
    for dx, dy in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        prod *= count(dx, dy)

    print(part1)
    print(prod)

if __name__ == '__main__':
    solve()
