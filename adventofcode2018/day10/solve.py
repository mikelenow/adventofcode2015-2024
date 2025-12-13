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

    points = []
    for line in lines:
        if not line:
            continue
        # position=< 9,  1> velocity=< 0,  2>
        p1 = line.find('<')
        p2 = line.find('>')
        v1 = line.find('<', p2)
        v2 = line.find('>', v1)
        x_str, y_str = line[p1 + 1:p2].split(',')
        vx_str, vy_str = line[v1 + 1:v2].split(',')
        x = int(x_str)
        y = int(y_str)
        vx = int(vx_str)
        vy = int(vy_str)
        points.append([x, y, vx, vy])

    def bounds(t: int):
        xs = []
        ys = []
        for x, y, vx, vy in points:
            xs.append(x + vx * t)
            ys.append(y + vy * t)
        return min(xs), max(xs), min(ys), max(ys)

    # Find time of minimal area (unimodal).
    t = 0
    best_t = 0
    min_x, max_x, min_y, max_y = bounds(0)
    best_area = (max_x - min_x) * (max_y - min_y)

    # Coarse forward scan until area starts increasing.
    while True:
        t += 1
        min_x, max_x, min_y, max_y = bounds(t)
        area = (max_x - min_x) * (max_y - min_y)
        if area < best_area:
            best_area = area
            best_t = t
        else:
            # If we've passed the minimum, stop.
            if t - best_t > 5:
                break

    min_x, max_x, min_y, max_y = bounds(best_t)
    coords = set()
    for x, y, vx, vy in points:
        coords.add((x + vx * best_t, y + vy * best_t))

    lines_out = []
    for yy in range(min_y, max_y + 1):
        row = []
        for xx in range(min_x, max_x + 1):
            row.append('#' if (xx, yy) in coords else '.')
        lines_out.append(''.join(row))

    print('\n'.join(lines_out))
    print(best_t)

if __name__ == '__main__':
    solve()
