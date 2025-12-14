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
            self.inputs = []
            self.halted = False

        def r(self, a):
            return self.mem.get(a, 0)

        def w(self, a, v):
            self.mem[a] = v

        def add_inputs(self, vals):
            self.inputs.extend(vals)

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
                    self.w(addr(m1, a), self.inputs.pop(0))
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

    def run_script(script_lines):
        vm = VM(program)
        script = '\n'.join(script_lines) + '\n'
        vm.add_inputs([ord(c) for c in script])
        last = 0
        while not vm.halted:
            v = vm.run_until_output()
            if v is None:
                if vm.halted:
                    break
                continue
            last = v
        return last

    script1 = [
        'NOT A J',
        'NOT B T',
        'OR T J',
        'NOT C T',
        'OR T J',
        'AND D J',
        'WALK',
    ]

    script2 = [
        'NOT A J',
        'NOT B T',
        'OR T J',
        'NOT C T',
        'OR T J',
        'AND D J',
        'NOT E T',
        'NOT T T',
        'OR H T',
        'AND T J',
        'RUN',
    ]

    part1 = run_script(script1)
    part2 = run_script(script2)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
