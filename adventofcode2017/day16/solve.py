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
        print("Part 1: ")
        print("Part 2: ")
        return

    moves = lines[0].split(',')

    def dance(state):
        arr = list(state)
        for m in moves:
            if m[0] == 's':
                x = int(m[1:])
                arr = arr[-x:] + arr[:-x]
            elif m[0] == 'x':
                a, b = map(int, m[1:].split('/'))
                arr[a], arr[b] = arr[b], arr[a]
            elif m[0] == 'p':
                a, b = m[1:].split('/')
                ia = arr.index(a)
                ib = arr.index(b)
                arr[ia], arr[ib] = arr[ib], arr[ia]
        return ''.join(arr)

    start = 'abcdefghijklmnop'
    part1 = dance(start)

    # Part 2: detect cycle
    seen = {start: 0}
    states = [start]
    cur = start
    total = 1_000_000_000
    i = 0
    while True:
        i += 1
        cur = dance(cur)
        if cur in seen:
            cycle_start = seen[cur]
            cycle_len = i - cycle_start
            remaining = (total - cycle_start) % cycle_len
            part2 = states[cycle_start + remaining]
            break
        seen[cur] = i
        states.append(cur)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
