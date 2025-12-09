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

    from collections import deque

    favorite = int(lines[0])

    def is_open(x, y, fav):
        if x < 0 or y < 0:
            return False
        num = x*x + 3*x + 2*x*y + y + y*y + fav
        bits = bin(num).count('1')
        return bits % 2 == 0

    def bfs(start, goal, fav):
        queue = deque([(start, 0)])
        visited = {start}
        locations_within_50 = set()

        while queue:
            (x, y), steps = queue.popleft()

            if steps <= 50:
                locations_within_50.add((x, y))

            if (x, y) == goal:
                return steps, len(locations_within_50)

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited and is_open(nx, ny, fav):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), steps + 1))

        return -1, len(locations_within_50)

    part1, part2 = bfs((1, 1), (31, 39), favorite)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
