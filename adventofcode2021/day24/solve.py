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
    prog = [s for s in lines if s]
    if not prog:
        print(0)
        print(0)
        return

    if len(prog) % 18 != 0:
        print(0)
        print(0)
        return

    n_blocks = len(prog) // 18
    params = []
    for i in range(n_blocks):
        block = prog[i * 18:(i + 1) * 18]
        divz = int(block[4].split()[-1])
        addx = int(block[5].split()[-1])
        addy = int(block[15].split()[-1])
        params.append((divz, addx, addy))

    max_digits = [0] * n_blocks
    min_digits = [0] * n_blocks
    stack = []
    for i, (divz, addx, addy) in enumerate(params):
        if divz == 1:
            stack.append((i, addy))
        elif divz == 26:
            j, prev_addy = stack.pop()
            delta = prev_addy + addx

            if delta >= 0:
                max_j = 9 - delta
                max_i = 9
                min_j = 1
                min_i = 1 + delta
            else:
                max_j = 9
                max_i = 9 + delta
                min_j = 1 - delta
                min_i = 1

            max_digits[j] = max_j
            max_digits[i] = max_i
            min_digits[j] = min_j
            min_digits[i] = min_i
        else:
            print(0)
            print(0)
            return

    for i in range(n_blocks):
        if max_digits[i] == 0:
            max_digits[i] = 9
        if min_digits[i] == 0:
            min_digits[i] = 1
        if not (1 <= max_digits[i] <= 9 and 1 <= min_digits[i] <= 9):
            print(0)
            print(0)
            return

    part1 = ''.join(str(d) for d in max_digits)
    part2 = ''.join(str(d) for d in min_digits)
    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
