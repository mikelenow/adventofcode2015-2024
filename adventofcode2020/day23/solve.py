import sys
from array import array

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
    s = ''
    for ln in lines:
        if ln:
            s = ln.strip()
            break
    if not s:
        print(0)
        print(0)
        return

    cups0 = [int(ch) for ch in s]

    def play(cups, moves, total=None):
        if total is None:
            total = len(cups)
        nxt = array('I', [0]) * (total + 1)
        last = cups[0]
        for v in cups[1:]:
            nxt[last] = v
            last = v
        if total > len(cups):
            for v in range(max(cups) + 1, total + 1):
                nxt[last] = v
                last = v
        nxt[last] = cups[0]

        cur = cups[0]
        mx = total
        for _ in range(moves):
            a = nxt[cur]
            b = nxt[a]
            c = nxt[b]
            after = nxt[c]
            nxt[cur] = after

            dest = cur - 1 or mx
            while dest == a or dest == b or dest == c:
                dest = dest - 1 or mx

            nxt[c] = nxt[dest]
            nxt[dest] = a
            cur = nxt[cur]

        return nxt

    nxt1 = play(cups0, 100)
    out = []
    x = nxt1[1]
    while x != 1:
        out.append(str(x))
        x = nxt1[x]
    part1 = ''.join(out)

    nxt2 = play(cups0, 10_000_000, 1_000_000)
    a = nxt2[1]
    b = nxt2[a]
    part2 = a * b

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
