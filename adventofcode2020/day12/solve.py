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
    inst = []
    for s in lines:
        if s:
            inst.append((s[0], int(s[1:])))
    if not inst:
        print(0)
        print(0)
        return

    x = 0
    y = 0
    dx = 1
    dy = 0

    def rot_right(vx, vy, deg):
        k = (deg // 90) % 4
        for _ in range(k):
            vx, vy = vy, -vx
        return vx, vy

    for op, n in inst:
        if op == 'N':
            y += n
        elif op == 'S':
            y -= n
        elif op == 'E':
            x += n
        elif op == 'W':
            x -= n
        elif op == 'F':
            x += dx * n
            y += dy * n
        elif op == 'R':
            dx, dy = rot_right(dx, dy, n)
        elif op == 'L':
            dx, dy = rot_right(dx, dy, 360 - n)

    part1 = abs(x) + abs(y)

    sx = 0
    sy = 0
    wx = 10
    wy = 1
    for op, n in inst:
        if op == 'N':
            wy += n
        elif op == 'S':
            wy -= n
        elif op == 'E':
            wx += n
        elif op == 'W':
            wx -= n
        elif op == 'F':
            sx += wx * n
            sy += wy * n
        elif op == 'R':
            wx, wy = rot_right(wx, wy, n)
        elif op == 'L':
            wx, wy = rot_right(wx, wy, 360 - n)

    part2 = abs(sx) + abs(sy)
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
