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

    rows = []
    for line in lines:
        if not line:
            continue
        parts = line.split()
        rows.append([int(x) for x in parts])

    # Part 1: checksum is sum of (max - min) per row
    checksum1 = 0
    for row in rows:
        checksum1 += max(row) - min(row)

    # Part 2: for each row, find the only pair where one evenly divides the other
    checksum2 = 0
    for row in rows:
        found = False
        length = len(row)
        for i in range(length):
            if found:
                break
            for j in range(length):
                if i == j:
                    continue
                a, b = row[i], row[j]
                if a % b == 0:
                    checksum2 += a // b
                    found = True
                    break

    print(f"Part 1: {checksum1}")
    print(f"Part 2: {checksum2}")

if __name__ == '__main__':
    solve()
