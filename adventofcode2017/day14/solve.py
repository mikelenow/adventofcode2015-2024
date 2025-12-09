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
    if not lines or not lines[0]:
        print("Part 1: 0")
        print("Part 2: 0")
        return

    key = lines[0].strip()

    def knot_hash(data):
        lengths = [ord(c) for c in data] + [17, 31, 73, 47, 23]
        nums = list(range(256))
        pos = 0
        skip = 0
        n = len(nums)
        for _ in range(64):
            for length in lengths:
                if length > n:
                    continue
                for i in range(length // 2):
                    a = (pos + i) % n
                    b = (pos + length - 1 - i) % n
                    nums[a], nums[b] = nums[b], nums[a]
                pos = (pos + length + skip) % n
                skip += 1
        dense = []
        for i in range(0, 256, 16):
            x = 0
            for v in nums[i:i+16]:
                x ^= v
            dense.append(x)
        return ''.join(f"{x:02x}" for x in dense)

    grid_bits = []
    part1 = 0
    for row in range(128):
        h = knot_hash(f"{key}-{row}")
        bits = ''.join(bin(int(ch, 16))[2:].zfill(4) for ch in h)
        grid_bits.append(bits)
        part1 += bits.count('1')

    # Part 2: count regions
    from collections import deque

    ones = {(r, c) for r in range(128) for c in range(128) if grid_bits[r][c] == '1'}
    regions = 0

    while ones:
        start = ones.pop()
        q = deque([start])
        while q:
            r, c = q.popleft()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 128 and 0 <= nc < 128 and (nr, nc) in ones:
                    ones.remove((nr, nc))
                    q.append((nr, nc))
        regions += 1

    part2 = regions

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
