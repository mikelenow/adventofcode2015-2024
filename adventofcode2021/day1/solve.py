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
    nums = [int(s) for s in lines if s]
    if not nums:
        print(0)
        print(0)
        return

    part1 = 0
    for a, b in zip(nums, nums[1:]):
        if b > a:
            part1 += 1

    part2 = 0
    for a, b in zip(nums, nums[3:]):
        if b > a:
            part2 += 1

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
