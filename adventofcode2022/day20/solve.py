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
    vals0 = [int(s) for s in lines if s]
    n = len(vals0)
    if n == 0:
        print(0)
        print(0)
        return

    def mix(values, rounds):
        ids = list(range(n))
        order = ids[:]
        for _ in range(rounds):
            for i in ids:
                v = values[i]
                if v == 0:
                    continue
                idx = order.index(i)
                order.pop(idx)
                new_idx = (idx + v) % (n - 1)
                order.insert(new_idx, i)
        return order

    def grove_sum(values, order):
        zero_id = None
        for i, v in enumerate(values):
            if v == 0:
                zero_id = i
                break
        zi = order.index(zero_id)
        s = 0
        for off in (1000, 2000, 3000):
            s += values[order[(zi + off) % n]]
        return s

    order1 = mix(vals0, 1)
    part1 = grove_sum(vals0, order1)

    key = 811589153
    vals2 = [v * key for v in vals0]
    order2 = mix(vals2, 10)
    part2 = grove_sum(vals2, order2)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
