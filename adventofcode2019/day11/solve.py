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
        print('')
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

    def run_robot(start_color: int):
        vm = VM(program)
        panels = {(0, 0): start_color}
        painted = set()
        x = y = 0
        dx, dy = 0, -1

        while not vm.halted:
            vm.add_input(panels.get((x, y), 0))
            c = vm.run_until_output()
            if c is None:
                break
            t = vm.run_until_output()
            if t is None:
                break
            panels[(x, y)] = c
            painted.add((x, y))
            if t == 0:
                dx, dy = -dy, dx
            else:
                dx, dy = dy, -dx
            x += dx
            y += dy
        return panels, painted

    panels1, painted1 = run_robot(0)
    part1 = len(painted1)

    panels2, _ = run_robot(1)
    whites = [p for p, v in panels2.items() if v == 1]
    if not whites:
        part2 = ''
    else:
        min_x = min(x for x, _ in whites)
        max_x = max(x for x, _ in whites)
        min_y = min(y for _, y in whites)
        max_y = max(y for _, y in whites)
        out = []
        for yy in range(min_y, max_y + 1):
            row = ''
            for xx in range(min_x, max_x + 1):
                row += '#' if panels2.get((xx, yy), 0) == 1 else ' '
            out.append(row.rstrip())
        part2 = '\n'.join(out)

    print(part1)
    print(part2)

if __name__ == '__main__':
    solve()
