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
    from collections import defaultdict

    regs = defaultdict(int)
    max_ever = None

    def check(cond_reg, op, val):
        x = regs[cond_reg]
        if op == '==':
            return x == val
        if op == '!=':
            return x != val
        if op == '>':
            return x > val
        if op == '<':
            return x < val
        if op == '>=':
            return x >= val
        if op == '<=':
            return x <= val
        return False

    for line in lines:
        if not line:
            continue
        parts = line.split()
        reg = parts[0]
        op = parts[1]
        val = int(parts[2])
        cond_reg = parts[4]
        cond_op = parts[5]
        cond_val = int(parts[6])

        if check(cond_reg, cond_op, cond_val):
            if op == 'inc':
                regs[reg] += val
            else:
                regs[reg] -= val
            if max_ever is None or regs[reg] > max_ever:
                max_ever = regs[reg]

    part1 = max(regs.values()) if regs else 0
    part2 = max_ever if max_ever is not None else part1

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
