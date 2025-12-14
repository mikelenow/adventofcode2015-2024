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

    nums = []
    for s in lines:
        if s:
            nums.append(int(s))

    if not nums:
        print(0)
        print(0)
        return

    seen = set()
    part1 = 0
    for x in nums:
        y = 2020 - x
        if y in seen:
            part1 = x * y
            break
        seen.add(x)

    part2 = 0
    s_all = set(nums)
    n = len(nums)
    for i in range(n):
        a = nums[i]
        for j in range(i + 1, n):
            b = nums[j]
            c = 2020 - a - b
            if c in s_all:
                part2 = a * b * c
                break
        if part2:
            break

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
