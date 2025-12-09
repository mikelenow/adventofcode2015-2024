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

    def is_valid_triangle(a, b, c):
        return a + b > c and a + c > b and b + c > a

    triangles = []
    for line in lines:
        if line:
            sides = list(map(int, line.split()))
            triangles.append(sides)

    part1 = sum(1 for tri in triangles if is_valid_triangle(*tri))

    part2_count = 0
    for col in range(3):
        for row in range(0, len(triangles), 3):
            if row + 2 < len(triangles):
                a = triangles[row][col]
                b = triangles[row + 1][col]
                c = triangles[row + 2][col]
                if is_valid_triangle(a, b, c):
                    part2_count += 1

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2_count}")

if __name__ == '__main__':
    solve()
