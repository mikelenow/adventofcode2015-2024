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
    workflows = {}
    parts = []

    i = 0
    while i < len(lines) and lines[i]:
        line = lines[i]
        name, rest = line.split('{', 1)
        rules_s = rest.strip('}')
        rules = []
        for item in rules_s.split(','):
            if ':' in item:
                cond, dest = item.split(':')
                var = cond[0]
                op = cond[1]
                val = int(cond[2:])
                rules.append((var, op, val, dest))
            else:
                rules.append((None, None, None, item))
        workflows[name] = rules
        i += 1

    while i < len(lines) and lines[i] == '':
        i += 1
    for line in lines[i:]:
        if not line:
            continue
        line = line.strip('{}')
        d = {}
        for kv in line.split(','):
            k, v = kv.split('=')
            d[k] = int(v)
        parts.append(d)

    def run_part(p):
        cur = 'in'
        while True:
            if cur == 'A':
                return True
            if cur == 'R':
                return False
            for var, op, val, dest in workflows[cur]:
                if var is None:
                    cur = dest
                    break
                x = p[var]
                ok = (x < val) if op == '<' else (x > val)
                if ok:
                    cur = dest
                    break

    part1 = 0
    for p in parts:
        if run_part(p):
            part1 += p['x'] + p['m'] + p['a'] + p['s']

    def count_ranges():
        from collections import deque

        def size(r):
            total = 1
            for lo, hi in r.values():
                if lo > hi:
                    return 0
                total *= (hi - lo + 1)
            return total

        start = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
        q = deque([('in', start)])
        total = 0

        while q:
            name, r = q.popleft()
            if name == 'A':
                total += size(r)
                continue
            if name == 'R':
                continue

            cur = r
            for var, op, val, dest in workflows[name]:
                if var is None:
                    q.append((dest, cur))
                    cur = None
                    break

                lo, hi = cur[var]
                if op == '<':
                    t_lo, t_hi = lo, min(hi, val - 1)
                    f_lo, f_hi = max(lo, val), hi
                else:
                    t_lo, t_hi = max(lo, val + 1), hi
                    f_lo, f_hi = lo, min(hi, val)

                if t_lo <= t_hi:
                    nr = dict(cur)
                    nr[var] = (t_lo, t_hi)
                    q.append((dest, nr))
                if f_lo <= f_hi:
                    cur = dict(cur)
                    cur[var] = (f_lo, f_hi)
                else:
                    cur = None
                    break

            if cur is None:
                continue

        return total

    part2 = count_ranges()

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
