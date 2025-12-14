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
    rules = {}
    i = 0
    rule_re = re.compile(r'^(.*): (\d+)-(\d+) or (\d+)-(\d+)$')
    while i < len(lines) and lines[i]:
        m = rule_re.match(lines[i])
        if m:
            name = m.group(1)
            a1 = int(m.group(2))
            b1 = int(m.group(3))
            a2 = int(m.group(4))
            b2 = int(m.group(5))
            rules[name] = ((a1, b1), (a2, b2))
        i += 1

    while i < len(lines) and lines[i] != 'your ticket:':
        i += 1
    i += 1
    your = [int(x) for x in lines[i].split(',')] if i < len(lines) and lines[i] else []
    i += 1

    while i < len(lines) and lines[i] != 'nearby tickets:':
        i += 1
    i += 1

    nearby = []
    for j in range(i, len(lines)):
        if lines[j]:
            nearby.append([int(x) for x in lines[j].split(',')])

    def valid_any(x):
        for (a1, b1), (a2, b2) in rules.values():
            if a1 <= x <= b1 or a2 <= x <= b2:
                return True
        return False

    part1 = 0
    good = []
    for t in nearby:
        bad = False
        for v in t:
            if not valid_any(v):
                part1 += v
                bad = True
        if not bad:
            good.append(t)

    part2 = 0
    if your and rules:
        cols = len(your)

        def valid_rule(name, x):
            (a1, b1), (a2, b2) = rules[name]
            return a1 <= x <= b1 or a2 <= x <= b2

        possible = [set(rules.keys()) for _ in range(cols)]
        for c in range(cols):
            for name in list(possible[c]):
                for t in good:
                    if not valid_rule(name, t[c]):
                        possible[c].remove(name)
                        break

        fixed = {}
        changed = True
        while changed:
            changed = False
            for c in range(cols):
                if c in fixed:
                    continue
                if len(possible[c]) == 1:
                    name = next(iter(possible[c]))
                    fixed[c] = name
                    for k in range(cols):
                        if k != c and name in possible[k]:
                            possible[k].remove(name)
                    changed = True

        part2 = 1
        for c, name in fixed.items():
            if name.startswith('departure'):
                part2 *= your[c]

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
