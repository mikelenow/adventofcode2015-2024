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

    ranges = []
    for line in lines:
        if line:
            start, end = map(int, line.split('-'))
            ranges.append((start, end))

    ranges.sort()

    # Merge overlapping ranges
    merged = []
    for start, end in ranges:
        if merged and start <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    # Part 1: First allowed IP
    part1 = merged[0][1] + 1 if merged[0][0] == 0 else 0

    # Part 2: Count allowed IPs
    max_ip = 4294967295
    blocked = sum(end - start + 1 for start, end in merged)
    part2 = max_ip + 1 - blocked

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
