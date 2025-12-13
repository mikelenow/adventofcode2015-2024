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
        x_str, y_str = line.split(',')
        points.append((int(x_str), int(y_str.strip())))

    if not points:
        print(0)
        print(0)
        return

    min_x = min(x for x, _ in points)
    max_x = max(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_y = max(y for _, y in points)

    area = [0] * len(points)
    infinite = set()

    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            best_i = None
            best_d = None
            tied = False
            for i, p in enumerate(points):
                d = abs(x - p[0]) + abs(y - p[1])
                if best_d is None or d < best_d:
                    best_d = d
                    best_i = i
                    tied = False
                elif d == best_d:
                    tied = True
            if not tied and best_i is not None:
                area[best_i] += 1
                if x == min_x or x == max_x or y == min_y or y == max_y:
                    infinite.add(best_i)

    part1 = 0
    for i, a in enumerate(area):
        if i not in infinite and a > part1:
            part1 = a

    threshold = 10000
    margin = threshold // len(points) + 1
    region = 0
    for y in range(min_y - margin, max_y + margin + 1):
        for x in range(min_x - margin, max_x + margin + 1):
            total = 0
            for px, py in points:
                total += abs(x - px) + abs(y - py)
                if total >= threshold:
                    break
            if total < threshold:
                region += 1

    print(part1)
    print(region)

if __name__ == '__main__':
    solve()
