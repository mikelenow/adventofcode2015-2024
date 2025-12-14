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

    paths = [line for line in lines if line]
    if len(paths) < 2:
        print(0)
        print(0)
        return

    def trace(path: str):
        x = y = 0
        steps = 0
        seen = {}
        for inst in path.split(','):
            d = inst[0]
            n = int(inst[1:])
            dx = dy = 0
            if d == 'U':
                dy = 1
            elif d == 'D':
                dy = -1
            elif d == 'L':
                dx = -1
            elif d == 'R':
                dx = 1
            else:
                raise ValueError(d)
            for _ in range(n):
                x += dx
                y += dy
                steps += 1
                if (x, y) not in seen:
                    seen[(x, y)] = steps
        return seen

    w1 = trace(paths[0])
    w2 = trace(paths[1])
    inter = set(w1.keys()) & set(w2.keys())
    if not inter:
        print(0)
        print(0)
        return

    part1 = min(abs(x) + abs(y) for (x, y) in inter)
    part2 = min(w1[p] + w2[p] for p in inter)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
