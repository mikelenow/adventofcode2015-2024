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

    clay = set()
    min_y = None
    max_y = None

    for line in lines:
        if not line:
            continue
        # x=495, y=2..7  OR  y=7, x=495..501
        first, second = [p.strip() for p in line.split(',')]
        if first.startswith('x='):
            x = int(first[2:])
            y1, y2 = second[2:].split('..')
            y1 = int(y1)
            y2 = int(y2)
            for y in range(y1, y2 + 1):
                clay.add((x, y))
        else:
            y = int(first[2:])
            x1, x2 = second[2:].split('..')
            x1 = int(x1)
            x2 = int(x2)
            for x in range(x1, x2 + 1):
                clay.add((x, y))

    for _, y in clay:
        if min_y is None or y < min_y:
            min_y = y
        if max_y is None or y > max_y:
            max_y = y

    if min_y is None:
        print(0)
        print(0)
        return

    flowing = set()
    settled = set()

    def blocked(p):
        return p in clay or p in settled

    visited = set()

    def flow_from(x: int, y: int):
        # Water enters at (x,y) and falls/spreads until it either escapes or settles.
        # We call this with y being the current position (can be above min_y).
        if (x, y) in visited:
            return
        visited.add((x, y))

        # Fall down
        cy = y
        while cy < max_y and not blocked((x, cy + 1)):
            cy += 1
            if cy >= min_y:
                flowing.add((x, cy))
        if cy >= max_y:
            return

        # Now we are supported from below at (x, cy+1); attempt to fill levels upward
        while True:
            # Spread left and right from (x, cy)
            lx = x
            while True:
                below = (lx, cy + 1)
                if not blocked(below):
                    break
                if (lx - 1, cy) in clay:
                    break
                lx -= 1

            rx = x
            while True:
                below = (rx, cy + 1)
                if not blocked(below):
                    break
                if (rx + 1, cy) in clay:
                    break
                rx += 1

            left_wall = (lx - 1, cy) in clay
            right_wall = (rx + 1, cy) in clay
            left_spill = not blocked((lx, cy + 1))
            right_spill = not blocked((rx, cy + 1))

            # Mark current row as flowing first
            for xx in range(lx, rx + 1):
                if cy >= min_y:
                    flowing.add((xx, cy))

            if left_wall and right_wall and not left_spill and not right_spill:
                # It is bounded: settle this row and move up
                for xx in range(lx, rx + 1):
                    if cy >= min_y:
                        settled.add((xx, cy))
                    flowing.discard((xx, cy))
                cy -= 1
                if cy < 0:
                    return
                if not blocked((x, cy + 1)):
                    return
                continue

            # Spill to sides (create new flows)
            if left_spill:
                flow_from(lx, cy)
            if right_spill:
                flow_from(rx, cy)
            return

    flow_from(500, 0)

    water = flowing | settled
    part1 = sum(1 for _, y in water if min_y <= y <= max_y)
    part2 = sum(1 for _, y in settled if min_y <= y <= max_y)
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
