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

    groups = []
    cur = []
    for s in lines + ['']:
        if s == '':
            if cur:
                groups.append(cur)
            cur = []
        else:
            cur.append(s)

    part1 = 0
    part2 = 0
    for g in groups:
        u = set()
        inter = None
        for p in g:
            st = set(p)
            u |= st
            if inter is None:
                inter = st
            else:
                inter &= st
        part1 += len(u)
        part2 += len(inter) if inter is not None else 0

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
