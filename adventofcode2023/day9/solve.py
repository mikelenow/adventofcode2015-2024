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
    seqs = []
    for line in lines:
        if not line:
            continue
        seqs.append([int(x) for x in line.split()])

    part1 = 0
    part2 = 0
    for seq in seqs:
        layers = [seq]
        while any(x != 0 for x in layers[-1]):
            prev = layers[-1]
            layers.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])

        nxt = 0
        for layer in reversed(layers):
            nxt += layer[-1]
        part1 += nxt

        prv = 0
        for layer in reversed(layers):
            prv = layer[0] - prv
        part2 += prv

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
