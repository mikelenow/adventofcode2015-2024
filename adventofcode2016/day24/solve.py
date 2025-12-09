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
    from itertools import permutations

    grid = [list(line) for line in lines if line]
    locations = {}

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell.isdigit():
                locations[int(cell)] = (x, y)

    def bfs(start, goal, grid):
        queue = deque([(start, 0)])
        visited = {start}

        while queue:
            (x, y), dist = queue.popleft()
            if (x, y) == goal:
                return dist

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                    if (nx, ny) not in visited and grid[ny][nx] != '#':
                        visited.add((nx, ny))
                        queue.append(((nx, ny), dist + 1))

        return float('inf')

    # Calculate distances between all pairs
    distances = {}
    for i in locations:
        for j in locations:
            if i != j:
                dist = bfs(locations[i], locations[j], grid)
                distances[(i, j)] = dist

    # Find shortest path visiting all locations
    other_locations = [i for i in locations if i != 0]

    part1 = float('inf')
    part2 = float('inf')

    for perm in permutations(other_locations):
        path = [0] + list(perm)
        dist = sum(distances[(path[i], path[i+1])] for i in range(len(path)-1))
        part1 = min(part1, dist)

        # Part 2: return to 0
        dist_return = dist + distances[(path[-1], 0)]
        part2 = min(part2, dist_return)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
