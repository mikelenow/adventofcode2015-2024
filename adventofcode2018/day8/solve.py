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

    data = []
    for line in lines:
        if line:
            data.extend(int(x) for x in line.split())

    idx = 0

    def parse_node():
        nonlocal idx
        child_count = data[idx]
        meta_count = data[idx + 1]
        idx += 2

        child_values = []
        meta_sum = 0
        for _ in range(child_count):
            s, v = parse_node()
            meta_sum += s
            child_values.append(v)

        meta = data[idx:idx + meta_count]
        idx += meta_count
        meta_sum += sum(meta)

        if child_count == 0:
            value = sum(meta)
        else:
            value = 0
            for m in meta:
                ci = m - 1
                if 0 <= ci < len(child_values):
                    value += child_values[ci]
        return meta_sum, value

    part1, part2 = parse_node()
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
