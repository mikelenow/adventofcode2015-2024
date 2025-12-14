import sys
import re

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
    foods = []
    pat = re.compile(r'^(.*) \(contains (.*)\)$')
    for s in lines:
        if not s:
            continue
        m = pat.match(s)
        if not m:
            continue
        ing = set(m.group(1).split())
        alg = [x.strip() for x in m.group(2).split(',')]
        foods.append((ing, alg))

    poss = {}
    for ing, algs in foods:
        for a in algs:
            if a not in poss:
                poss[a] = set(ing)
            else:
                poss[a] &= ing

    maybe_bad = set()
    for s in poss.values():
        maybe_bad |= s

    part1 = 0
    for ing, _ in foods:
        for x in ing:
            if x not in maybe_bad:
                part1 += 1

    fixed = {}
    while True:
        progress = False
        for a, s in poss.items():
            if a in fixed:
                continue
            s2 = s - set(fixed.values())
            poss[a] = s2
            if len(s2) == 1:
                fixed[a] = next(iter(s2))
                progress = True
        if not progress:
            break

    part2 = ','.join(fixed[a] for a in sorted(fixed))
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
