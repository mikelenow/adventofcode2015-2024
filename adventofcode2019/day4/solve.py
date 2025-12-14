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

    s = None
    for line in lines:
        if line:
            s = line
            break
    if not s or '-' not in s:
        print(0)
        print(0)
        return
    lo_s, hi_s = s.split('-')
    lo = int(lo_s)
    hi = int(hi_s)

    def digits(n: int):
        return [int(c) for c in str(n)]

    def nondecreasing(ds):
        return all(ds[i] <= ds[i + 1] for i in range(len(ds) - 1))

    def has_pair(ds):
        for i in range(len(ds) - 1):
            if ds[i] == ds[i + 1]:
                return True
        return False

    def has_exact_pair(ds):
        i = 0
        while i < len(ds):
            j = i
            while j < len(ds) and ds[j] == ds[i]:
                j += 1
            if j - i == 2:
                return True
            i = j
        return False

    part1 = 0
    part2 = 0
    for n in range(lo, hi + 1):
        ds = digits(n)
        if not nondecreasing(ds):
            continue
        if has_pair(ds):
            part1 += 1
        if has_exact_pair(ds):
            part2 += 1

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
