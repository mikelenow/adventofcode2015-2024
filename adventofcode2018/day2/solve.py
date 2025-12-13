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

    box_ids = [line for line in lines if line]

    twos = 0
    threes = 0
    for s in box_ids:
        counts = {}
        for ch in s:
            counts[ch] = counts.get(ch, 0) + 1
        values = set(counts.values())
        if 2 in values:
            twos += 1
        if 3 in values:
            threes += 1
    part1 = twos * threes

    # Part 2: find the two IDs that differ by exactly one character.
    # For each string, remove one position and use (index, remainder) as a key.
    seen = {}
    part2 = None
    for s in box_ids:
        for i in range(len(s)):
            key = (i, s[:i] + s[i+1:])
            if key in seen:
                part2 = key[1]
                break
            seen[key] = s
        if part2 is not None:
            break

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
