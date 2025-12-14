import sys
from collections import Counter

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
    template = ''
    i = 0
    while i < len(lines) and lines[i] == '':
        i += 1
    if i < len(lines):
        template = lines[i]
        i += 1
    while i < len(lines) and lines[i] == '':
        i += 1

    rules = {}
    for j in range(i, len(lines)):
        s = lines[j]
        if not s:
            continue
        a, b = s.split(' -> ')
        rules[a] = b

    if not template:
        print(0)
        print(0)
        return

    pairs = Counter()
    for a, b in zip(template, template[1:]):
        pairs[a + b] += 1
    last = template[-1]

    def step(p):
        out = Counter()
        for k, v in p.items():
            ins = rules.get(k)
            if ins is None:
                out[k] += v
            else:
                out[k[0] + ins] += v
                out[ins + k[1]] += v
        return out

    def score(p):
        cnt = Counter()
        for k, v in p.items():
            cnt[k[0]] += v
        cnt[last] += 1
        mx = max(cnt.values())
        mn = min(cnt.values())
        return mx - mn

    p = pairs
    for _ in range(10):
        p = step(p)
    part1 = score(p)

    for _ in range(40 - 10):
        p = step(p)
    part2 = score(p)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
