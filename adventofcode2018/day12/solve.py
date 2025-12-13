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

    initial = None
    rules = {}
    for line in lines:
        if not line:
            continue
        if line.startswith('initial state:'):
            initial = line.split(':', 1)[1].strip()
        elif '=>' in line:
            pat, res = [x.strip() for x in line.split('=>')]
            rules[pat] = res

    if initial is None:
        print(0)
        print(0)
        return

    pots = set(i for i, ch in enumerate(initial) if ch == '#')

    def step(pots_set):
        if not pots_set:
            return set()
        new = set()
        lo = min(pots_set)
        hi = max(pots_set)
        for i in range(lo - 2, hi + 3):
            pat = []
            for d in range(-2, 3):
                pat.append('#' if (i + d) in pots_set else '.')
            pat_s = ''.join(pat)
            if rules.get(pat_s, '.') == '#':
                new.add(i)
        return new

    def score(pots_set):
        return sum(pots_set)

    part1 = None
    target2 = 50_000_000_000

    last = score(pots)
    last_delta = None
    stable_count = 0

    gen = 0
    while gen < target2:
        gen += 1
        pots = step(pots)
        s = score(pots)
        delta = s - last

        if gen == 20:
            part1 = s

        if delta == last_delta:
            stable_count += 1
        else:
            stable_count = 0
            last_delta = delta

        # If the delta has stabilized for a while, extrapolate.
        if stable_count >= 100:
            remaining = target2 - gen
            part2 = s + remaining * delta
            print(part1)
            print(part2)
            return

        last = s

    # Fallback (if no stabilization detected)
    print(part1 if part1 is not None else score(pots))
    print(score(pots))

if __name__ == '__main__':
    solve()
