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
    prog = [line.split() for line in lines if line]

    from collections import defaultdict

    def get_val(regs, x):
        if x.lstrip('-').isdigit():
            return int(x)
        return regs[x]

    # Part 1: simulate with a=0 and count mul
    regs1 = defaultdict(int)
    ip = 0
    mul_count = 0
    while 0 <= ip < len(prog):
        inst = prog[ip]
        op = inst[0]
        x = inst[1]
        y = inst[2] if len(inst) > 2 else None

        if op == 'set':
            regs1[x] = get_val(regs1, y)
        elif op == 'sub':
            regs1[x] -= get_val(regs1, y)
        elif op == 'mul':
            regs1[x] *= get_val(regs1, y)
            mul_count += 1
        elif op == 'jnz':
            if get_val(regs1, x) != 0:
                ip += get_val(regs1, y)
                continue
        ip += 1

    part1 = mul_count

    # Part 2: analyze program; it counts non-primes in a range
    # From the input, with a=1, b starts at 84*100+100000 and c = b+17000
    b_start = 84 * 100 + 100000
    c = b_start + 17000

    def is_prime(n):
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        d = 3
        while d * d <= n:
            if n % d == 0:
                return False
            d += 2
        return True

    h = 0
    for b in range(b_start, c + 1, 17):
        if not is_prime(b):
            h += 1

    part2 = h

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
