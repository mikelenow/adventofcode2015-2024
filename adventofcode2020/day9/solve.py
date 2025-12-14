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

    nums = [int(s) for s in lines if s]
    if not nums:
        print(0)
        print(0)
        return

    pre = 25
    part1 = 0
    from collections import Counter
    cnt = Counter(nums[:pre])

    def ok(target):
        for a in cnt:
            b = target - a
            if b in cnt and (b != a or cnt[a] > 1):
                return True
        return False

    bad_idx = None
    for i in range(pre, len(nums)):
        x = nums[i]
        if not ok(x):
            part1 = x
            bad_idx = i
            break
        old = nums[i - pre]
        cnt[old] -= 1
        if cnt[old] == 0:
            del cnt[old]
        cnt[x] += 1

    part2 = 0
    if bad_idx is not None:
        target = part1
        lo = 0
        hi = 0
        s = 0
        while hi <= bad_idx:
            if s < target:
                s += nums[hi]
                hi += 1
            elif s > target:
                s -= nums[lo]
                lo += 1
            else:
                if hi - lo >= 2:
                    seq = nums[lo:hi]
                    part2 = min(seq) + max(seq)
                break

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
