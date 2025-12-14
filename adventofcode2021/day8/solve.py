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
    entries = []
    for s in lines:
        if not s:
            continue
        left, right = s.split(' | ')
        pats = [frozenset(x) for x in left.split()]
        outs = [frozenset(x) for x in right.split()]
        entries.append((pats, outs))

    part1 = 0
    for _, outs in entries:
        for o in outs:
            if len(o) in (2, 3, 4, 7):
                part1 += 1

    part2 = 0
    for pats, outs in entries:
        by_len = {}
        for p in pats:
            by_len.setdefault(len(p), []).append(p)

        one = by_len[2][0]
        four = by_len[4][0]
        seven = by_len[3][0]
        eight = by_len[7][0]

        sixes = by_len.get(6, [])
        fives = by_len.get(5, [])

        nine = next(p for p in sixes if four <= p)
        zero = next(p for p in sixes if p != nine and one <= p)
        six = next(p for p in sixes if p != nine and p != zero)

        three = next(p for p in fives if one <= p)
        five = next(p for p in fives if p != three and p <= six)
        two = next(p for p in fives if p != three and p != five)

        mp = {
            zero: 0,
            one: 1,
            two: 2,
            three: 3,
            four: 4,
            five: 5,
            six: 6,
            seven: 7,
            eight: 8,
            nine: 9,
        }

        v = 0
        for o in outs:
            v = v * 10 + mp[o]
        part2 += v

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
