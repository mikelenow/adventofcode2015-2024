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
    if not lines:
        print(0)
        print(0)
        return

    seeds = [int(x) for x in lines[0].split(':', 1)[1].split()]

    maps = []
    i = 1
    while i < len(lines):
        if not lines[i]:
            i += 1
            continue
        if lines[i].endswith('map:'):
            i += 1
            rules = []
            while i < len(lines) and lines[i]:
                d, s, ln = (int(x) for x in lines[i].split())
                rules.append((s, s + ln, d - s))
                i += 1
            rules.sort()
            maps.append(rules)
        else:
            i += 1

    def apply_value(x, rules):
        for s0, s1, delta in rules:
            if s0 <= x < s1:
                return x + delta
        return x

    part1 = None
    for seed in seeds:
        x = seed
        for rules in maps:
            x = apply_value(x, rules)
        if part1 is None or x < part1:
            part1 = x

    def normalize(intervals):
        if not intervals:
            return []
        intervals.sort()
        out = [intervals[0]]
        for a, b in intervals[1:]:
            pa, pb = out[-1]
            if a <= pb:
                if b > pb:
                    out[-1] = (pa, b)
            else:
                out.append((a, b))
        return out

    def apply_intervals(intervals, rules):
        res = []
        for a, b in intervals:
            x = a
            for s0, s1, delta in rules:
                if s1 <= x:
                    continue
                if s0 >= b:
                    break
                if x < s0:
                    res.append((x, min(s0, b)))
                    x = min(s0, b)
                    if x >= b:
                        break
                ov_a = max(x, s0)
                ov_b = min(b, s1)
                if ov_a < ov_b:
                    res.append((ov_a + delta, ov_b + delta))
                    x = ov_b
                    if x >= b:
                        break
            if x < b:
                res.append((x, b))
        return normalize(res)

    intervals = []
    for j in range(0, len(seeds), 2):
        intervals.append((seeds[j], seeds[j] + seeds[j + 1]))
    intervals = normalize(intervals)

    for rules in maps:
        intervals = apply_intervals(intervals, rules)

    part2 = min(a for a, b in intervals)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
