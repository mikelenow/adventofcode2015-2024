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

    def parse_regs(s: str):
        # "Before: [3, 2, 1, 1]" / "After:  [3, 2, 2, 1]"
        left = s.find('[')
        right = s.find(']')
        return [int(x.strip()) for x in s[left + 1:right].split(',')]

    def op_apply(name, regs, a, b, c):
        r = regs[:]
        if name == 'addr':
            r[c] = r[a] + r[b]
        elif name == 'addi':
            r[c] = r[a] + b
        elif name == 'mulr':
            r[c] = r[a] * r[b]
        elif name == 'muli':
            r[c] = r[a] * b
        elif name == 'banr':
            r[c] = r[a] & r[b]
        elif name == 'bani':
            r[c] = r[a] & b
        elif name == 'borr':
            r[c] = r[a] | r[b]
        elif name == 'bori':
            r[c] = r[a] | b
        elif name == 'setr':
            r[c] = r[a]
        elif name == 'seti':
            r[c] = a
        elif name == 'gtir':
            r[c] = 1 if a > r[b] else 0
        elif name == 'gtri':
            r[c] = 1 if r[a] > b else 0
        elif name == 'gtrr':
            r[c] = 1 if r[a] > r[b] else 0
        elif name == 'eqir':
            r[c] = 1 if a == r[b] else 0
        elif name == 'eqri':
            r[c] = 1 if r[a] == b else 0
        elif name == 'eqrr':
            r[c] = 1 if r[a] == r[b] else 0
        else:
            raise ValueError(name)
        return r

    op_names = [
        'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
        'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr'
    ]

    i = 0
    samples = []
    while i < len(lines):
        line = lines[i]
        if line.startswith('Before:'):
            before = parse_regs(line)
            instr = [int(x) for x in lines[i + 1].split()]
            after = parse_regs(lines[i + 2])
            samples.append((before, instr, after))
            i += 3
        elif line == '':
            i += 1
        else:
            break

    program = []
    while i < len(lines):
        if lines[i]:
            program.append([int(x) for x in lines[i].split()])
        i += 1

    part1 = 0
    possible = {n: set(op_names) for n in range(16)}
    for before, instr, after in samples:
        opcode, a, b, c = instr
        matches = []
        for name in op_names:
            if op_apply(name, before, a, b, c) == after:
                matches.append(name)
        if len(matches) >= 3:
            part1 += 1
        possible[opcode].intersection_update(matches)

    mapping = {}
    changed = True
    while changed:
        changed = False
        singles = [op for op, opts in possible.items() if len(opts) == 1 and op not in mapping]
        for op in singles:
            name = next(iter(possible[op]))
            mapping[op] = name
            for other in possible:
                if other != op and name in possible[other]:
                    possible[other].remove(name)
                    changed = True

    regs = [0, 0, 0, 0]
    for opcode, a, b, c in program:
        regs = op_apply(mapping[opcode], regs, a, b, c)

    print(part1)
    print(regs[0])

if __name__ == '__main__':
    solve()
