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
    cmds = []
    for s in lines:
        if not s:
            continue
        a, b = s.split()
        cmds.append((a, int(b)))

    x = 0
    d = 0
    for op, n in cmds:
        if op == 'forward':
            x += n
        elif op == 'down':
            d += n
        elif op == 'up':
            d -= n
    part1 = x * d

    x = 0
    d = 0
    aim = 0
    for op, n in cmds:
        if op == 'forward':
            x += n
            d += aim * n
        elif op == 'down':
            aim += n
        elif op == 'up':
            aim -= n
    part2 = x * d

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
