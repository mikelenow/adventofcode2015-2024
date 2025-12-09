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
    infected_init = set()
    n = len(lines)
    if n == 0:
        print("Part 1: 0")
        print("Part 2: 0")
        return

    offset = n // 2
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == '#':
                infected_init.add((c - offset, r - offset))

    # Directions: up, right, down, left
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def part1_bursts(bursts):
        infected = set(infected_init)
        x = y = 0
        dir_idx = 0  # up
        infections = 0
        for _ in range(bursts):
            if (x, y) in infected:
                # turn right, clean
                dir_idx = (dir_idx + 1) % 4
                infected.remove((x, y))
            else:
                # turn left, infect
                dir_idx = (dir_idx - 1) % 4
                infected.add((x, y))
                infections += 1
            dx, dy = dirs[dir_idx]
            x += dx
            y += dy
        return infections

    def part2_bursts(bursts):
        # 0: clean, 1: weakened, 2: infected, 3: flagged
        states = {}
        for (x, y) in infected_init:
            states[(x, y)] = 2
        x = y = 0
        dir_idx = 0
        infections = 0
        for _ in range(bursts):
            state = states.get((x, y), 0)
            if state == 0:  # clean
                dir_idx = (dir_idx - 1) % 4
                states[(x, y)] = 1
            elif state == 1:  # weakened
                # no turn
                states[(x, y)] = 2
                infections += 1
            elif state == 2:  # infected
                dir_idx = (dir_idx + 1) % 4
                states[(x, y)] = 3
            elif state == 3:  # flagged
                dir_idx = (dir_idx + 2) % 4
                # becomes clean
                states.pop((x, y), None)
            dx, dy = dirs[dir_idx]
            x += dx
            y += dy
        return infections

    part1 = part1_bursts(10_000)
    part2 = part2_bursts(10_000_000)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
