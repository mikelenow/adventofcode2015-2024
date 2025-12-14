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
    hands = []
    for line in lines:
        if not line:
            continue
        h, b = line.split()
        hands.append((h, int(b)))

    def kind_rank_from_counts(counts):
        counts = sorted(counts, reverse=True)
        if counts[0] == 5:
            return 6
        if counts[0] == 4:
            return 5
        if counts[0] == 3 and counts[1] == 2:
            return 4
        if counts[0] == 3:
            return 3
        if counts[0] == 2 and counts[1] == 2:
            return 2
        if counts[0] == 2:
            return 1
        return 0

    def classify(hand):
        from collections import Counter
        c = Counter(hand)
        return kind_rank_from_counts(c.values())

    order1 = {c: i for i, c in enumerate('23456789TJQKA')}
    order2 = {c: i for i, c in enumerate('J23456789TQKA')}

    def key1(item):
        h, bid = item
        return (classify(h), [order1[c] for c in h])

    def classify_joker(hand):
        from collections import Counter
        j = hand.count('J')
        if j == 5:
            return 6
        c = Counter(ch for ch in hand if ch != 'J')
        counts = sorted(c.values(), reverse=True)
        counts[0] += j
        return kind_rank_from_counts(counts)

    def key2(item):
        h, bid = item
        return (classify_joker(h), [order2[c] for c in h])

    part1 = 0
    for i, (h, bid) in enumerate(sorted(hands, key=key1), 1):
        part1 += i * bid

    part2 = 0
    for i, (h, bid) in enumerate(sorted(hands, key=key2), 1):
        part2 += i * bid

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
