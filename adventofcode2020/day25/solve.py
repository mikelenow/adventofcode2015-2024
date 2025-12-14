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
    vals = [int(s) for s in lines if s]
    if len(vals) < 2:
        print(0)
        print(0)
        return

    card, door = vals[0], vals[1]
    mod = 20201227
    subj = 7

    v = 1
    loop = 0
    while v != card:
        v = (v * subj) % mod
        loop += 1

    key = pow(door, loop, mod)
    print(key)
    print(0)

if __name__ == '__main__':
    solve()
