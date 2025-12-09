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

    from collections import Counter

    if not lines:
        return

    message_length = len(lines[0])
    part1 = []
    part2 = []

    for i in range(message_length):
        column = [line[i] for line in lines if len(line) > i]
        counter = Counter(column)
        most_common = counter.most_common(1)[0][0]
        least_common = counter.most_common()[-1][0]
        part1.append(most_common)
        part2.append(least_common)

    print(f"Part 1: {''.join(part1)}")
    print(f"Part 2: {''.join(part2)}")

if __name__ == '__main__':
    solve()
