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
    offsets = [int(line) for line in lines if line]

    # Part 1
    data1 = offsets[:]
    steps1 = 0
    idx = 0
    n = len(data1)
    while 0 <= idx < n:
        jump = data1[idx]
        data1[idx] += 1
        idx += jump
        steps1 += 1

    # Part 2
    data2 = offsets[:]
    steps2 = 0
    idx = 0
    n2 = len(data2)
    while 0 <= idx < n2:
        jump = data2[idx]
        if jump >= 3:
            data2[idx] -= 1
        else:
            data2[idx] += 1
        idx += jump
        steps2 += 1

    print(f"Part 1: {steps1}")
    print(f"Part 2: {steps2}")

if __name__ == '__main__':
    solve()
