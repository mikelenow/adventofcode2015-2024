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

    nums = sorted(int(s) for s in lines if s)
    if not nums:
        print(0)
        print(0)
        return

    nums = [0] + nums + [nums[-1] + 3]
    d1 = 0
    d3 = 0
    for a, b in zip(nums, nums[1:]):
        d = b - a
        if d == 1:
            d1 += 1
        elif d == 3:
            d3 += 1
    part1 = d1 * d3

    ways = {0: 1}
    for x in nums[1:]:
        ways[x] = ways.get(x - 1, 0) + ways.get(x - 2, 0) + ways.get(x - 3, 0)
    part2 = ways[nums[-1]]

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
