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
        def __init__(self, prog, inputs=None):
            self.mem = {i: v for i, v in enumerate(prog)}
            self.ip = 0
            self.rb = 0
            self.inputs = list(inputs) if inputs else []
            self.halted = False

        def r(self, a):
            return self.mem.get(a, 0)

        def w(self, a, v):
            self.mem[a] = v

        def add_input(self, v):
            self.inputs.append(v)

        def run_until_blocked(self):
            outs = []

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
                    return outs
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
                        return outs
                    a = self.r(self.ip + 1)
                    self.w(addr(m1, a), self.inputs.pop(0))
                    self.ip += 2
                elif op == 4:
                    a = self.r(self.ip + 1)
                    outs.append(get(m1, a))
                    self.ip += 2
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

    n = 50
    vms = [VM(program, [i]) for i in range(n)]
    queues = [deque() for _ in range(n)]
    outbufs = [[] for _ in range(n)]

    part1 = None
    nat = None
    last_nat_y = None
    part2 = None

    while part2 is None:
        idle = True
        for i in range(n):
            if queues[i]:
                idle = False
                while queues[i]:
                    vms[i].add_input(queues[i].popleft())
            else:
                vms[i].add_input(-1)

            outs = vms[i].run_until_blocked()
            if outs:
                idle = False
            buf = outbufs[i]
            buf.extend(outs)
            while len(buf) >= 3:
                dest, x, y = buf[0], buf[1], buf[2]
                del buf[:3]
                if dest == 255:
                    if part1 is None:
                        part1 = y
                    nat = (x, y)
                elif 0 <= dest < n:
                    queues[dest].append(x)
                    queues[dest].append(y)

        if idle and nat is not None:
            x, y = nat
            queues[0].append(x)
            queues[0].append(y)
            if last_nat_y == y:
                part2 = y
            last_nat_y = y

    print(part1 if part1 is not None else 0)
    print(part2)

if __name__ == '__main__':
    solve()