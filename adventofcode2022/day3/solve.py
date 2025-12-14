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
    def prio(ch):
        o = ord(ch)
        if 97 <= o <= 122:
            return o - 96
        return o - 38

    p1 = 0
    sacks = [s for s in lines if s]
    for s in sacks:
        n = len(s)
        a = set(s[:n // 2])
        b = set(s[n // 2:])
        c = (a & b).pop()
        p1 += prio(c)

    p2 = 0
    for i in range(0, len(sacks), 3):
        g = sacks[i:i + 3]
        if len(g) < 3:
            break
        c = (set(g[0]) & set(g[1]) & set(g[2])).pop()
        p2 += prio(c)

    print(p1)
    print(p2)

if __name__ == '__main__':
    solve()
