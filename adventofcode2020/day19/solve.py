import sys
import re
from functools import lru_cache

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
    while i < len(lines) and lines[i]:
        s = lines[i]
        idx, rhs = s.split(':', 1)
        idx = int(idx)
        rhs = rhs.strip()
        if '"' in rhs:
            rules[idx] = rhs.replace('"', '').strip()
        else:
            alts = []
            for part in rhs.split('|'):
                seq = [int(x) for x in part.strip().split()] if part.strip() else []
                alts.append(seq)
            rules[idx] = alts
        i += 1

    while i < len(lines) and lines[i] == '':
        i += 1
    msgs = [s for s in lines[i:] if s]

    def count_matches(rules_local):
        def match_message(msg):
            @lru_cache(None)
            def match(rule_id, pos):
                r = rules_local[rule_id]
                if isinstance(r, str):
                    if pos < len(msg) and msg[pos] == r:
                        return (pos + 1,)
                    return ()

                out = set()
                for seq in r:
                    positions = {pos}
                    for sub in seq:
                        nxt = set()
                        for p in positions:
                            for q in match(sub, p):
                                nxt.add(q)
                        positions = nxt
                        if not positions:
                            break
                    out |= positions
                return tuple(out)

            return len(msg) in match(0, 0)

        return sum(1 for m in msgs if match_message(m))

    part1 = count_matches(rules)

    rules2 = dict(rules)
    if 8 in rules2 and 11 in rules2:
        rules2[8] = [[42], [42, 8]]
        rules2[11] = [[42, 31], [42, 11, 31]]
    part2 = count_matches(rules2)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
