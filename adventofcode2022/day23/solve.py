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
    grid = [s for s in lines if s]
    elves = set()
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == '#':
                elves.add((x, y))
    if not elves:
        print(0)
        print(0)
        return

    neigh8 = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    checks = [
        ([( -1, -1), (0, -1), (1, -1)], (0, -1)),
        ([( -1,  1), (0,  1), (1,  1)], (0,  1)),
        ([( -1, -1), (-1, 0), (-1, 1)], (-1, 0)),
        ([(  1, -1), ( 1, 0), ( 1, 1)], ( 1, 0)),
    ]

    round_no = 0
    part1 = None
    while True:
        props = {}
        counts = {}
        moved_any = False
        for x, y in elves:
            if all((x + dx, y + dy) not in elves for dx, dy in neigh8):
                continue
            for k in range(4):
                cells, step = checks[(round_no + k) % 4]
                if all((x + dx, y + dy) not in elves for dx, dy in cells):
                    nx, ny = x + step[0], y + step[1]
                    props[(x, y)] = (nx, ny)
                    counts[(nx, ny)] = counts.get((nx, ny), 0) + 1
                    break

        new_elves = set(elves)
        for src, dst in props.items():
            if counts[dst] == 1:
                new_elves.remove(src)
                new_elves.add(dst)
                moved_any = True
        elves = new_elves

        round_no += 1
        if round_no == 10:
            xs = [x for x, _ in elves]
            ys = [y for _, y in elves]
            area = (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1)
            part1 = area - len(elves)
        if not moved_any:
            part2 = round_no
            print(part1 if part1 is not None else 0)
            print(part2)
            return

if __name__ == '__main__':
    solve()
