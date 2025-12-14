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

    base_program = [int(x) for x in line.split(',')]

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

        def add_input(self, v):
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

    def run_collect(prog, joystick=None):
        vm = VM(prog)
        out = []
        score = 0
        paddle_x = 0
        ball_x = 0
        tiles = {}
        while not vm.halted:
            v = vm.run_until_output()
            if v is None:
                if vm.halted:
                    break
                if joystick is not None:
                    j = -1 if ball_x < paddle_x else (1 if ball_x > paddle_x else 0)
                    vm.add_input(j)
                continue
            out.append(v)
            if len(out) == 3:
                x, y, t = out
                out = []
                if x == -1 and y == 0:
                    score = t
                else:
                    tiles[(x, y)] = t
                    if t == 3:
                        paddle_x = x
                    elif t == 4:
                        ball_x = x
        return tiles, score

    tiles1, _ = run_collect(base_program)
    part1 = sum(1 for v in tiles1.values() if v == 2)

    prog2 = base_program[:]
    prog2[0] = 2
    _, part2 = run_collect(prog2, joystick=True)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
