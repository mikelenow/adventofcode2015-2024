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
    limits = {'red': 12, 'green': 13, 'blue': 14}

    part1 = 0
    part2 = 0
    for line in lines:
        if not line:
            continue
        head, rest = line.split(':', 1)
        game_id = int(head.split()[1])
        draws = rest.strip().split(';')

        ok = True
        maxc = {'red': 0, 'green': 0, 'blue': 0}
        for draw in draws:
            for item in draw.strip().split(','):
                item = item.strip()
                if not item:
                    continue
                n_s, color = item.split()
                n = int(n_s)
                if n > limits[color]:
                    ok = False
                if n > maxc[color]:
                    maxc[color] = n

        if ok:
            part1 += game_id
        part2 += maxc['red'] * maxc['green'] * maxc['blue']

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
