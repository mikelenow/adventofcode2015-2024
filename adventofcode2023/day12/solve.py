import sys
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
    rows = []
    for line in lines:
        if not line:
            continue
        pat, nums = line.split()
        groups = tuple(int(x) for x in nums.split(','))
        rows.append((pat, groups))

    def count_arrangements(pat, groups):
        n = len(pat)
        m = len(groups)

        @lru_cache(None)
        def dp(i, gi, run):
            if i == n:
                if run:
                    if gi < m and run == groups[gi] and gi + 1 == m:
                        return 1
                    return 0
                return 1 if gi == m else 0

            total = 0
            ch = pat[i]

            if ch in '.?':
                if run:
                    if gi < m and run == groups[gi]:
                        total += dp(i + 1, gi + 1, 0)
                else:
                    total += dp(i + 1, gi, 0)

            if ch in '#?':
                if gi < m and run < groups[gi]:
                    total += dp(i + 1, gi, run + 1)

            return total

        return dp(0, 0, 0)

    part1 = 0
    part2 = 0
    for pat, groups in rows:
        part1 += count_arrangements(pat, groups)
        pat2 = '?'.join([pat] * 5)
        groups2 = groups * 5
        part2 += count_arrangements(pat2, groups2)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
