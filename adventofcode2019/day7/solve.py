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
    from itertools import permutations

    program = []
    for line in lines:
        if line:
            program = [int(x) for x in line.split(',')]
            break
    if not program:
        print(0)
        print(0)
        return

    class VM:
        def __init__(self, prog, inputs):
            self.mem = prog[:]
            self.ip = 0
            self.inputs = list(inputs)
            self.halted = False

        def add_input(self, v):
            self.inputs.append(v)

        def run_until_output(self):
            def get(mode, val):
                return self.mem[val] if mode == 0 else val

            while True:
                instr = self.mem[self.ip]
                op = instr % 100
                m1 = (instr // 100) % 10
                m2 = (instr // 1000) % 10
                if op == 99:
                    self.halted = True
                    return None
                if op in (1, 2, 7, 8):
                    a = self.mem[self.ip + 1]
                    b = self.mem[self.ip + 2]
                    c = self.mem[self.ip + 3]
                    va = get(m1, a)
                    vb = get(m2, b)
                    if op == 1:
                        self.mem[c] = va + vb
                    elif op == 2:
                        self.mem[c] = va * vb
                    elif op == 7:
                        self.mem[c] = 1 if va < vb else 0
                    else:
                        self.mem[c] = 1 if va == vb else 0
                    self.ip += 4
                elif op == 3:
                    if not self.inputs:
                        return None
                    a = self.mem[self.ip + 1]
                    self.mem[a] = self.inputs.pop(0)
                    self.ip += 2
                elif op == 4:
                    a = self.mem[self.ip + 1]
                    self.ip += 2
                    return get(m1, a)
                elif op in (5, 6):
                    a = self.mem[self.ip + 1]
                    b = self.mem[self.ip + 2]
                    va = get(m1, a)
                    vb = get(m2, b)
                    if (op == 5 and va != 0) or (op == 6 and va == 0):
                        self.ip = vb
                    else:
                        self.ip += 3
                else:
                    raise ValueError(op)

    # Part 1
    best1 = 0
    for phases in permutations([0, 1, 2, 3, 4]):
        signal = 0
        for ph in phases:
            vm = VM(program, [ph, signal])
            outv = vm.run_until_output()
            signal = outv if outv is not None else 0
        best1 = max(best1, signal)

    best2 = 0
    for phases in permutations([5, 6, 7, 8, 9]):
        vms = [VM(program, [ph]) for ph in phases]
        signal = 0
        last = 0
        idx = 0
        while not vms[4].halted:
            vm = vms[idx]
            vm.add_input(signal)
            outv = vm.run_until_output()
            if outv is not None:
                signal = outv
                if idx == 4:
                    last = outv
            idx = (idx + 1) % 5
        best2 = max(best2, last)

    print(best1)
    print(best2)

if __name__ == '__main__':
    solve()
