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
        print("Part 1: 0")
        print("Part 2: 0")
        return

    data = lines[0].strip()

    def knot_round(nums, lengths, pos=0, skip=0):
        n = len(nums)
        for length in lengths:
            if length > n:
                continue
            # reverse section
            for i in range(length // 2):
                a = (pos + i) % n
                b = (pos + length - 1 - i) % n
                nums[a], nums[b] = nums[b], nums[a]
            pos = (pos + length + skip) % n
            skip += 1
        return pos, skip

    # Part 1
    lengths1 = [int(x) for x in data.split(',') if x]
    nums1 = list(range(256))
    knot_round(nums1, lengths1)
    part1 = nums1[0] * nums1[1]

    # Part 2: full Knot Hash
    lengths2 = [ord(c) for c in data] + [17, 31, 73, 47, 23]
    nums2 = list(range(256))
    pos = 0
    skip = 0
    for _ in range(64):
        pos, skip = knot_round(nums2, lengths2, pos, skip)

    dense = []
    for i in range(0, 256, 16):
        x = 0
        for v in nums2[i:i+16]:
            x ^= v
        dense.append(x)

    part2 = ''.join(f"{x:02x}" for x in dense)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
