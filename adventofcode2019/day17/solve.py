import sys
from collections import deque

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
    line = ''
    for s in lines:
        if s:
            line = s
            break
    if not line:
        print(0)
        print(0)
        return

    program = [int(x) for x in line.split(',')]

    class VM:
        def __init__(self, prog):
            self.mem = {i: v for i, v in enumerate(prog)}
            self.ip = 0
            self.rb = 0
            self.inputs = deque()
            self.halted = False

        def r(self, a):
            return self.mem.get(a, 0)

        def w(self, a, v):
            self.mem[a] = v

        def add_inputs(self, vals):
            for v in vals:
                self.inputs.append(v)

        def run_until_output(self):
            def get(mode, param):
                if mode == 0:
                    return self.r(param)
                if mode == 1:
                    return param
                if mode == 2:
                    return self.r(self.rb + param)
                raise ValueError(mode)

            def addr(mode, param):
                if mode == 0:
                    return param
                if mode == 2:
                    return self.rb + param
                raise ValueError(mode)

            while True:
                instr = self.r(self.ip)
                op = instr % 100
                m1 = (instr // 100) % 10
                m2 = (instr // 1000) % 10
                m3 = (instr // 10000) % 10
                if op == 99:
                    self.halted = True
                    return None
                if op in (1, 2, 7, 8):
                    a = self.r(self.ip + 1)
                    b = self.r(self.ip + 2)
                    c = self.r(self.ip + 3)
                    va = get(m1, a)
                    vb = get(m2, b)
                    dest = addr(m3, c)
                    if op == 1:
                        self.w(dest, va + vb)
                    elif op == 2:
                        self.w(dest, va * vb)
                    elif op == 7:
                        self.w(dest, 1 if va < vb else 0)
                    else:
                        self.w(dest, 1 if va == vb else 0)
                    self.ip += 4
                elif op == 3:
                    if not self.inputs:
                        return None
                    a = self.r(self.ip + 1)
                    self.w(addr(m1, a), self.inputs.popleft())
                    self.ip += 2
                elif op == 4:
                    a = self.r(self.ip + 1)
                    self.ip += 2
                    return get(m1, a)
                elif op in (5, 6):
                    a = self.r(self.ip + 1)
                    b = self.r(self.ip + 2)
                    va = get(m1, a)
                    vb = get(m2, b)
                    if (op == 5 and va != 0) or (op == 6 and va == 0):
                        self.ip = vb
                    else:
                        self.ip += 3
                elif op == 9:
                    a = self.r(self.ip + 1)
                    self.rb += get(m1, a)
                    self.ip += 2
                else:
                    raise ValueError(op)

    vm = VM(program)
    out_chars = []
    while not vm.halted:
        v = vm.run_until_output()
        if v is None:
            break
        out_chars.append(chr(v))
    text = ''.join(out_chars)
    grid_lines = [ln for ln in text.splitlines() if ln]
    if not grid_lines:
        print(0)
        print(0)
        return

    h = len(grid_lines)
    w = max(len(r) for r in grid_lines)
    grid = [list(r.ljust(w)) for r in grid_lines]

    scaff = set()
    start = None
    start_dir = None
    dirs = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}
    for y in range(h):
        for x in range(w):
            ch = grid[y][x]
            if ch == '#':
                scaff.add((x, y))
            elif ch in dirs:
                scaff.add((x, y))
                start = (x, y)
                start_dir = dirs[ch]

    part1 = 0
    for x, y in scaff:
        if (x - 1, y) in scaff and (x + 1, y) in scaff and (x, y - 1) in scaff and (x, y + 1) in scaff:
            part1 += x * y

    def derive_path():
        x, y = start
        dx, dy = start_dir
        tokens = []
        while True:
            left = (dy, -dx)
            right = (-dy, dx)

            def can_step(ndx, ndy):
                return (x + ndx, y + ndy) in scaff

            if can_step(left[0], left[1]):
                tokens.append('L')
                dx, dy = left
            elif can_step(right[0], right[1]):
                tokens.append('R')
                dx, dy = right
            else:
                break

            steps = 0
            while can_step(dx, dy):
                x += dx
                y += dy
                steps += 1
            tokens.append(str(steps))
        return tokens

    path = derive_path()

    def encode(seq):
        return ','.join(seq)

    def find_routines(tokens):
        names = ['A', 'B', 'C']

        def rec(i, funcs, main):
            if i == len(tokens):
                if len(encode(main)) <= 20:
                    return main, funcs
                return None

            for name, seq in funcs.items():
                if tokens[i:i + len(seq)] == seq:
                    nm = main + [name]
                    if len(encode(nm)) <= 20:
                        res = rec(i + len(seq), funcs, nm)
                        if res is not None:
                            return res

            if len(funcs) < 3:
                name = names[len(funcs)]
                for j in range(i + 2, len(tokens) + 1):
                    seq = tokens[i:j]
                    if len(encode(seq)) > 20:
                        break
                    nm = main + [name]
                    if len(encode(nm)) > 20:
                        continue
                    nfuncs = dict(funcs)
                    nfuncs[name] = seq
                    res = rec(j, nfuncs, nm)
                    if res is not None:
                        return res
            return None

        return rec(0, {}, [])

    res = find_routines(path)

    if res is None:
        part2 = 0
    else:
        main, funcs = res
        main_s = encode(main)
        a_s = encode(funcs.get('A', []))
        b_s = encode(funcs.get('B', []))
        c_s = encode(funcs.get('C', []))
        inp = main_s + '\n' + a_s + '\n' + b_s + '\n' + c_s + '\n' + 'n\n'
        vm2 = VM(program[:])
        vm2.mem[0] = 2
        vm2.add_inputs([ord(ch) for ch in inp])
        last = 0
        while not vm2.halted:
            v = vm2.run_until_output()
            if v is None:
                break
            last = v
        part2 = last

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
