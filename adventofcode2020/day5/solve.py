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

    passes = [s for s in lines if s]
    if not passes:
        print(0)
        print(0)
        return

    ids = []
    for s in passes:
        row_s = s[:7].replace('F', '0').replace('B', '1')
        col_s = s[7:].replace('L', '0').replace('R', '1')
        row = int(row_s, 2)
        col = int(col_s, 2)
        ids.append(row * 8 + col)

    ids.sort()
    part1 = ids[-1]
    part2 = 0
    for a, b in zip(ids, ids[1:]):
        if b == a + 2:
            part2 = a + 1
            break

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
