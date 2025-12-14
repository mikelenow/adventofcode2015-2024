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

    times = [int(x) for x in lines[0].split(':', 1)[1].split()]
    dists = [int(x) for x in lines[1].split(':', 1)[1].split()]

    def dist_for(t, hold):
        return hold * (t - hold)

    def count_wins(t, record):
        lo = 0
        hi = t
        while lo < hi:
            mid = (lo + hi) // 2
            if dist_for(t, mid) > record:
                hi = mid
            else:
                lo = mid + 1
        left = lo

        lo = 0
        hi = t
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if dist_for(t, mid) > record:
                lo = mid
            else:
                hi = mid - 1
        right = lo
        if left > right:
            return 0
        return right - left + 1

    part1 = 1
    for t, d in zip(times, dists):
        part1 *= count_wins(t, d)

    t2 = int(''.join(str(x) for x in times))
    d2 = int(''.join(str(x) for x in dists))
    part2 = count_wins(t2, d2)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
