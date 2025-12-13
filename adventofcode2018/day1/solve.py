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

    changes = []
    for line in lines:
        if not line:
            continue
        changes.append(int(line))

    part1 = sum(changes)

    seen = {0}
    freq = 0
    part2 = None
    if changes:
        i = 0
        while True:
            freq += changes[i]
            if freq in seen:
                part2 = freq
                break
            seen.add(freq)
            i = (i + 1) % len(changes)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
