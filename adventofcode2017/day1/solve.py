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

    data = lines[0].strip()

    # Part 1: sum digits that match the next digit (circular)
    total1 = 0
    n = len(data)
    for i, ch in enumerate(data):
        if ch == data[(i + 1) % n]:
            total1 += int(ch)

    # Part 2: sum digits that match the digit halfway around the list
    total2 = 0
    step = n // 2
    for i, ch in enumerate(data):
        if ch == data[(i + step) % n]:
            total2 += int(ch)

    print(f"Part 1: {total1}")
    print(f"Part 2: {total2}")

if __name__ == '__main__':
    solve()
