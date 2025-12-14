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

    contains = {}
    parents = {}
    pat = re.compile(r'^(.*) bags contain (.*)\.$')
    sub = re.compile(r'^(\d+) (.*) bag')

    for s in lines:
        if not s:
            continue
        m = pat.match(s)
        if not m:
            continue
        outer = m.group(1)
        rest = m.group(2)
        kids = []
        if rest != 'no other bags':
            parts = rest.split(', ')
            for p in parts:
                m2 = sub.match(p)
                if m2:
                    n = int(m2.group(1))
                    color = m2.group(2)
                    kids.append((color, n))
                    parents.setdefault(color, set()).add(outer)
        contains[outer] = kids

    seen = set()
    stack = list(parents.get('shiny gold', set()))
    while stack:
        c = stack.pop()
        if c in seen:
            continue
        seen.add(c)
        stack.extend(parents.get(c, set()))
    part1 = len(seen)

    memo = {}
    def total_inside(color):
        v = memo.get(color)
        if v is not None:
            return v
        total = 0
        for child, n in contains.get(color, []):
            total += n * (1 + total_inside(child))
        memo[color] = total
        return total

    part2 = total_inside('shiny gold')
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
