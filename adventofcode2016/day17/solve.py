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

    import hashlib
    from collections import deque

    passcode = lines[0]

    def get_open_doors(path, passcode):
        hash_input = passcode + path
        h = hashlib.md5(hash_input.encode()).hexdigest()[:4]
        doors = []
        if h[0] in 'bcdef':
            doors.append('U')
        if h[1] in 'bcdef':
            doors.append('D')
        if h[2] in 'bcdef':
            doors.append('L')
        if h[3] in 'bcdef':
            doors.append('R')
        return doors

    def solve_vault(passcode):
        queue = deque([(0, 0, '')])
        shortest = None
        longest_len = 0

        while queue:
            x, y, path = queue.popleft()

            if x == 3 and y == 3:
                if shortest is None:
                    shortest = path
                longest_len = max(longest_len, len(path))
                continue

            open_doors = get_open_doors(path, passcode)

            for door in open_doors:
                nx, ny, new_path = x, y, path + door
                if door == 'U' and y > 0:
                    ny = y - 1
                elif door == 'D' and y < 3:
                    ny = y + 1
                elif door == 'L' and x > 0:
                    nx = x - 1
                elif door == 'R' and x < 3:
                    nx = x + 1
                else:
                    continue

                queue.append((nx, ny, new_path))

        return shortest, longest_len

    part1, part2 = solve_vault(passcode)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
