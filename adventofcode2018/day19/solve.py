import sys
from typing import Optional

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

    ip_reg = int(lines[0].split()[1])
    program = []
    for line in lines[1:]:
        if not line:
            continue
        op, a, b, c = line.split()
        program.append((op, int(a), int(b), int(c)))

    def op_apply(op, regs, a, b, c):
        r = regs
        if op == 'addr':
            r[c] = r[a] + r[b]
        elif op == 'addi':
            r[c] = r[a] + b
        elif op == 'mulr':
            r[c] = r[a] * r[b]
        elif op == 'muli':
            r[c] = r[a] * b
        elif op == 'banr':
            r[c] = r[a] & r[b]
        elif op == 'bani':
            r[c] = r[a] & b
        elif op == 'borr':
            r[c] = r[a] | r[b]
        elif op == 'bori':
            r[c] = r[a] | b
        elif op == 'setr':
            r[c] = r[a]
        elif op == 'seti':
            r[c] = a
        elif op == 'gtir':
            r[c] = 1 if a > r[b] else 0
        elif op == 'gtri':
            r[c] = 1 if r[a] > b else 0
        elif op == 'gtrr':
            r[c] = 1 if r[a] > r[b] else 0
        elif op == 'eqir':
            r[c] = 1 if a == r[b] else 0
        elif op == 'eqri':
            r[c] = 1 if r[a] == b else 0
        elif op == 'eqrr':
            r[c] = 1 if r[a] == r[b] else 0
        else:
            raise ValueError(op)

    def run(reg0: int, stop_ip: Optional[int] = None, max_steps: Optional[int] = None):
        regs = [0, 0, 0, 0, 0, 0]
        regs[0] = reg0
        ip = 0
        steps = 0
        while 0 <= ip < len(program):
            if stop_ip is not None and ip == stop_ip:
                break
            regs[ip_reg] = ip
            op, a, b, c = program[ip]
            op_apply(op, regs, a, b, c)
            ip = regs[ip_reg]
            ip += 1
            steps += 1
            if max_steps is not None and steps >= max_steps:
                break
        return regs

    # Part 1: full run with reg0=0
    part1 = run(0)[0]

    # Part 2: program computes sum of divisors of a target in register 4.
    # For reg0=1, run just the initialization until IP reaches 1 (start of main loop).
    regs = run(1, stop_ip=1)
    target = regs[4]

    total = 0
    d = 1
    while d * d <= target:
        if target % d == 0:
            total += d
            other = target // d
            if other != d:
                total += other
        d += 1

    print(part1)
    print(total)

if __name__ == '__main__':
    solve()
