import sys
import math

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

    instr = lines[0].strip()
    mapping = {}
    for line in lines[1:]:
        if not line:
            continue
        a, rest = line.split('=', 1)
        a = a.strip()
        rest = rest.strip()
        rest = rest.strip('() ')
        left, right = [x.strip() for x in rest.split(',')]
        mapping[a] = (left, right)

    def walk(start, is_end):
        node = start
        step = 0
        L = len(instr)
        seen = {}
        z_hits = []
        while True:
            state = (node, step % L)
            if state in seen:
                cyc_start = seen[state]
                cyc_len = step - cyc_start
                return z_hits, cyc_start, cyc_len
            seen[state] = step
            if is_end(node) and step > 0:
                z_hits.append(step)
            turn = instr[step % L]
            node = mapping[node][0] if turn == 'L' else mapping[node][1]
            step += 1

    node = 'AAA'
    part1 = 0
    if node in mapping:
        step = 0
        while node != 'ZZZ':
            turn = instr[step % len(instr)]
            node = mapping[node][0] if turn == 'L' else mapping[node][1]
            step += 1
        part1 = step

    starts = [k for k in mapping.keys() if k.endswith('A')]
    periods = []
    for s in starts:
        hits, cyc_start, cyc_len = walk(s, lambda x: x.endswith('Z'))
        if not hits:
            periods.append(0)
            continue
        periods.append(hits[0])

    part2 = 0
    if periods and all(p > 0 for p in periods):
        part2 = periods[0]
        for p in periods[1:]:
            part2 = math.lcm(part2, p)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
