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
    pairs = []
    cur = []
    for s in lines + ['']:
        if s == '':
            if len(cur) == 2:
                pairs.append((cur[0], cur[1]))
            cur = []
        else:
            cur.append(s)

    import ast

    def cmp(a, b):
        if isinstance(a, int) and isinstance(b, int):
            return -1 if a < b else (1 if a > b else 0)
        if isinstance(a, int):
            a = [a]
        if isinstance(b, int):
            b = [b]
        i = 0
        while i < len(a) and i < len(b):
            r = cmp(a[i], b[i])
            if r != 0:
                return r
            i += 1
        if i == len(a) and i == len(b):
            return 0
        return -1 if i == len(a) else 1

    part1 = 0
    packets = []
    for i, (a, b) in enumerate(pairs, 1):
        pa = ast.literal_eval(a)
        pb = ast.literal_eval(b)
        packets.append(pa)
        packets.append(pb)
        if cmp(pa, pb) == -1:
            part1 += i

    div1 = [[2]]
    div2 = [[6]]
    packets.append(div1)
    packets.append(div2)

    from functools import cmp_to_key
    packets.sort(key=cmp_to_key(cmp))

    i1 = packets.index(div1) + 1
    i2 = packets.index(div2) + 1
    part2 = i1 * i2

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
