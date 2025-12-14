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
    algo = ''
    i = 0
    while i < len(lines) and lines[i] == '':
        i += 1
    if i < len(lines):
        algo = lines[i]
        i += 1
    while i < len(lines) and lines[i] == '':
        i += 1
    img_lines = [s for s in lines[i:] if s]

    if not algo or not img_lines:
        print(0)
        print(0)
        return

    diff = set()
    for y, row in enumerate(img_lines):
        for x, ch in enumerate(row):
            if ch == '#':
                diff.add((x, y))

    bg = 0

    def enhance(diff_set, bg_bit):
        xs = [x for x, _ in diff_set]
        ys = [y for _, y in diff_set]
        if xs:
            minx = min(xs)
            maxx = max(xs)
            miny = min(ys)
            maxy = max(ys)
        else:
            minx = maxx = miny = maxy = 0

        def get(x, y):
            return bg_bit ^ (1 if (x, y) in diff_set else 0)

        if bg_bit == 0:
            new_bg = 1 if algo[0] == '#' else 0
        else:
            new_bg = 1 if algo[511] == '#' else 0

        new_diff = set()
        for y in range(miny - 1, maxy + 2):
            for x in range(minx - 1, maxx + 2):
                idx = 0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        idx <<= 1
                        nx = x + dx
                        ny = y + dy
                        idx |= get(nx, ny)
                new_val = 1 if algo[idx] == '#' else 0
                if new_val != new_bg:
                    new_diff.add((x, y))

        return new_diff, new_bg

    part1 = 0
    cur = diff
    cur_bg = bg
    for step in range(1, 51):
        cur, cur_bg = enhance(cur, cur_bg)
        if step == 2:
            if cur_bg != 0:
                raise RuntimeError('Infinite background is lit at step 2; lit pixel count is not finite')
            part1 = len(cur)
    if cur_bg != 0:
        raise RuntimeError('Infinite background is lit at step 50; lit pixel count is not finite')
    part2 = len(cur)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
