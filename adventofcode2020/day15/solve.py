import sys
from array import array

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

    start = [int(x) for x in first.split(',')]

    target1 = 2020
    target2 = 30000000

    last_seen = array('I', [0]) * (target2 + 1)
    for i in range(len(start) - 1):
        last_seen[start[i]] = i + 1
    last = start[-1]

    part1 = 0
    turn = len(start)
    while turn < target2:
        prev = last_seen[last]
        last_seen[last] = turn
        last = 0 if prev == 0 else (turn - prev)
        turn += 1
        if turn == target1:
            part1 = last
    part2 = last

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
