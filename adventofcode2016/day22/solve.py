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

    import re

    nodes = []
    for line in lines[2:]:  # Skip header
        if line:
            match = re.search(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T', line)
            if match:
                x, y, size, used, avail = map(int, match.groups())
                nodes.append((x, y, size, used, avail))

    # Part 1: Count viable pairs
    viable = 0
    for i, (x1, y1, s1, u1, a1) in enumerate(nodes):
        if u1 == 0:
            continue
        for j, (x2, y2, s2, u2, a2) in enumerate(nodes):
            if i != j and u1 <= a2:
                viable += 1

    # Part 2: Grid sliding puzzle
    # Find the empty node and the wall (nodes too large to move)
    grid = {}
    empty_pos = None
    max_x = 0
    max_y = 0

    for x, y, size, used, avail in nodes:
        grid[(x, y)] = (size, used, avail)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        if used == 0:
            empty_pos = (x, y)

    # Find wall of immovable nodes (nodes with size > 100T are typically walls)
    wall_threshold = 100
    wall_nodes = set()
    for (x, y), (size, used, avail) in grid.items():
        if size > wall_threshold:
            wall_nodes.add((x, y))

    # Part 2 calculation:
    # 1. Move empty node from its position to (max_x-1, 0)
    #    - Must go around the wall
    # 2. Then perform the "5-step shuffle" to move goal data left
    #    - Takes 5 steps per position to move goal data one position left
    # 3. Goal data starts at (max_x, 0) and needs to reach (0, 0)

    # Step 1: Find path length for empty to reach (max_x-1, 0)
    # Most inputs have wall blocking direct path, need to go around
    from collections import deque

    def bfs_empty_to_goal_adjacent(start, goal_x):
        queue = deque([(start, 0)])
        visited = {start}

        while queue:
            (x, y), steps = queue.popleft()

            if x == goal_x - 1 and y == 0:
                return steps

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited and (nx, ny) in grid and (nx, ny) not in wall_nodes:
                    if 0 <= nx <= max_x and 0 <= ny <= max_y:
                        visited.add((nx, ny))
                        queue.append(((nx, ny), steps + 1))

        return 0

    steps_to_adjacent = bfs_empty_to_goal_adjacent(empty_pos, max_x)

    # Step 2: Shuffle data from (max_x, 0) to (0, 0)
    # First move: empty at (max_x-1, 0), swap with goal at (max_x, 0) = 1 move
    # Then for each remaining position: 5 moves to shuffle left once
    # Need to move goal data from position max_x to position 0 = max_x moves
    # After first swap, goal is at (max_x-1, 0), need (max_x-1) more swaps
    # Each swap (after the first) takes 5 moves to reposition empty
    shuffle_steps = 1 + (max_x - 1) * 5

    part2 = steps_to_adjacent + shuffle_steps

    print(f"Part 1: {viable}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
