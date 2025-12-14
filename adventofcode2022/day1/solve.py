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
    totals = []
    cur = 0
    for s in lines + ['']:
        if s == '':
            totals.append(cur)
            cur = 0
        else:
            cur += int(s)

    totals.sort(reverse=True)
    part1 = totals[0] if totals else 0
    part2 = sum(totals[:3]) if totals else 0
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
