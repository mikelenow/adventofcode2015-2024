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
    bits = [s for s in lines if s]
    if not bits:
        print(0)
        print(0)
        return

    n = len(bits[0])
    ones = [0] * n
    for s in bits:
        for i, ch in enumerate(s):
            if ch == '1':
                ones[i] += 1

    gamma = 0
    eps = 0
    for i in range(n):
        gamma <<= 1
        eps <<= 1
        if ones[i] * 2 >= len(bits):
            gamma |= 1
        else:
            eps |= 1
    eps = ((1 << n) - 1) ^ gamma
    part1 = gamma * eps

    def oxy_rating():
        cand = bits[:]
        for i in range(n):
            if len(cand) == 1:
                break
            c1 = sum(1 for s in cand if s[i] == '1')
            c0 = len(cand) - c1
            want = '1' if c1 >= c0 else '0'
            cand = [s for s in cand if s[i] == want]
        return int(cand[0], 2)

    def co2_rating():
        cand = bits[:]
        for i in range(n):
            if len(cand) == 1:
                break
            c1 = sum(1 for s in cand if s[i] == '1')
            c0 = len(cand) - c1
            want = '0' if c0 <= c1 else '1'
            cand = [s for s in cand if s[i] == want]
        return int(cand[0], 2)

    oxy = oxy_rating()
    co2 = co2_rating()
    part2 = oxy * co2

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
