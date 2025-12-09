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

    instructions = lines[0].split(', ')

    x, y = 0, 0
    direction = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    visited = {(0, 0)}
    part2 = None

    for instruction in instructions:
        turn = instruction[0]
        blocks = int(instruction[1:])

        if turn == 'R':
            direction = (direction + 1) % 4
        else:
            direction = (direction - 1) % 4

        dx, dy = directions[direction]

        # Move one block at a time for Part 2
        for _ in range(blocks):
            x += dx
            y += dy
            if part2 is None and (x, y) in visited:
                part2 = abs(x) + abs(y)
            visited.add((x, y))

    distance = abs(x) + abs(y)
    print(f"Part 1: {distance}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
