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
    cards = []
    for line in lines:
        if not line:
            continue
        _, rest = line.split(':', 1)
        left, right = rest.split('|')
        win = set(int(x) for x in left.split())
        have = [int(x) for x in right.split()]
        m = sum(1 for x in have if x in win)
        cards.append(m)

    part1 = 0
    for m in cards:
        if m:
            part1 += 1 << (m - 1)

    counts = [1] * len(cards)
    for i, m in enumerate(cards):
        ci = counts[i]
        for j in range(1, m + 1):
            if i + j < len(counts):
                counts[i + j] += ci
    part2 = sum(counts)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
