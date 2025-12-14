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
    clean = [s for s in lines if s]
    if len(clean) < 2:
        print(0)
        print(0)
        return

    t0 = int(clean[0])
    buses = clean[1].split(',')

    best_wait = None
    best_bus = None
    for b in buses:
        if b == 'x':
            continue
        n = int(b)
        wait = (-t0) % n
        if best_wait is None or wait < best_wait:
            best_wait = wait
            best_bus = n
    part1 = (best_wait or 0) * (best_bus or 0)

    def egcd(a, b):
        if b == 0:
            return a, 1, 0
        g, x1, y1 = egcd(b, a % b)
        return g, y1, x1 - (a // b) * y1

    def inv(a, mod):
        g, x, _ = egcd(a, mod)
        if g != 1:
            raise ValueError('no inverse')
        return x % mod

    r = 0
    m = 1
    for i, b in enumerate(buses):
        if b == 'x':
            continue
        n = int(b)
        a = (-i) % n
        k = ((a - r) % n) * inv(m % n, n) % n
        r = r + m * k
        m *= n
        r %= m

    part2 = r
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
