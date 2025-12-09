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

    # Day 3: Perfectly Spherical Houses in a Vacuum
    # Part 1: Count unique houses visited by Santa
    # Part 2: Count unique houses visited by Santa and Robo-Santa alternating

    data = lines[0]

    # Part 1: Solo Santa
    x, y = 0, 0
    visited = {(0, 0)}
    for char in data:
        if char == '^':
            y += 1
        elif char == 'v':
            y -= 1
        elif char == '>':
            x += 1
        elif char == '<':
            x -= 1
        visited.add((x, y))

    part1 = len(visited)

    # Part 2: Santa and Robo-Santa
    santa_x, santa_y = 0, 0
    robo_x, robo_y = 0, 0
    visited2 = {(0, 0)}

    for i, char in enumerate(data):
        if i % 2 == 0:  # Santa's turn
            if char == '^':
                santa_y += 1
            elif char == 'v':
                santa_y -= 1
            elif char == '>':
                santa_x += 1
            elif char == '<':
                santa_x -= 1
            visited2.add((santa_x, santa_y))
        else:  # Robo-Santa's turn
            if char == '^':
                robo_y += 1
            elif char == 'v':
                robo_y -= 1
            elif char == '>':
                robo_x += 1
            elif char == '<':
                robo_x -= 1
            visited2.add((robo_x, robo_y))

    part2 = len(visited2)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
