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
    first = ''
    for s in lines:
        if s:
            first = s
            break
    if not first:
        print(0)
        print(0)
        return

    nums = [int(x) for x in first.split(',') if x]
    counts = [0] * 9
    for n in nums:
        counts[n] += 1

    def step(c):
        z = c[0]
        c = c[1:] + [z]
        c[6] += z
        return c

    c = counts
    for _ in range(80):
        c = step(c)
    part1 = sum(c)

    for _ in range(256 - 80):
        c = step(c)
    part2 = sum(c)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
