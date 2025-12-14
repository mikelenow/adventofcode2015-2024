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

    part1 = 0
    part2 = 0

    for s in lines:
        if not s:
            continue
        policy, pw = s.split(':', 1)
        pw = pw.strip()
        rng, ch = policy.split()
        lo_s, hi_s = rng.split('-')
        lo = int(lo_s)
        hi = int(hi_s)

        cnt = pw.count(ch)
        if lo <= cnt <= hi:
            part1 += 1

        a = lo - 1
        b = hi - 1
        ca = (0 <= a < len(pw) and pw[a] == ch)
        cb = (0 <= b < len(pw) and pw[b] == ch)
        if ca ^ cb:
            part2 += 1

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
