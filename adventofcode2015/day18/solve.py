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

    # Day 18: Like a GIF For Your Yard
    # Conway's Game of Life with lights

    def count_neighbors(grid, r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc]:
                    count += 1
        return count

    def step(grid, stuck_corners=False):
        new_grid = [[False] * len(grid[0]) for _ in range(len(grid))]
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if stuck_corners and (r, c) in [(0, 0), (0, len(grid[0])-1), (len(grid)-1, 0), (len(grid)-1, len(grid[0])-1)]:
                    new_grid[r][c] = True
                else:
                    neighbors = count_neighbors(grid, r, c)
                    if grid[r][c]:
                        new_grid[r][c] = neighbors in [2, 3]
                    else:
                        new_grid[r][c] = neighbors == 3
        return new_grid

    # Parse initial grid
    initial_grid = [[c == '#' for c in line] for line in lines]

    # Part 1: 100 steps
    grid = [row[:] for row in initial_grid]
    for _ in range(100):
        grid = step(grid)
    part1 = sum(sum(row) for row in grid)

    # Part 2: 100 steps with corners stuck on
    grid = [row[:] for row in initial_grid]
    # Turn on corners
    grid[0][0] = grid[0][-1] = grid[-1][0] = grid[-1][-1] = True
    for _ in range(100):
        grid = step(grid, stuck_corners=True)
    part2 = sum(sum(row) for row in grid)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
