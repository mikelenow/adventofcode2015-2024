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
    program = []
    for line in lines:
        if line:
            program = [int(x) for x in line.split(',')]
            break
    if not program:
        print(0)
        print(0)
        return

    def run(inputs):
        mem = {}
        for i, v in enumerate(program):
            mem[i] = v
        ip = 0
        rb = 0
        inp = list(inputs)
        outputs = []

        def r(addr):
            return mem.get(addr, 0)

        def w(addr, val):
            mem[addr] = val

        def get(mode, param):
            if mode == 0:
                return r(param)
            if mode == 1:
                return param
            if mode == 2:
                return r(rb + param)
            raise ValueError(mode)

        def addr(mode, param):
            if mode == 0:
                return param
            if mode == 2:
                return rb + param
            raise ValueError(mode)

        while True:
            instr = r(ip)
            op = instr % 100
            m1 = (instr // 100) % 10
            m2 = (instr // 1000) % 10
            m3 = (instr // 10000) % 10

            if op == 99:
                break
            if op in (1, 2, 7, 8):
                a = r(ip + 1)
                b = r(ip + 2)
                c = r(ip + 3)
                va = get(m1, a)
                vb = get(m2, b)
                dest = addr(m3, c)
                if op == 1:
                    w(dest, va + vb)
                elif op == 2:
                    w(dest, va * vb)
                elif op == 7:
                    w(dest, 1 if va < vb else 0)
                else:
                    w(dest, 1 if va == vb else 0)
                ip += 4
            elif op == 3:
                a = r(ip + 1)
                if not inp:
                    raise ValueError('missing input')
                w(addr(m1, a), inp.pop(0))
                ip += 2
            elif op == 4:
                a = r(ip + 1)
                outputs.append(get(m1, a))
                ip += 2
            elif op in (5, 6):
                a = r(ip + 1)
                b = r(ip + 2)
                va = get(m1, a)
                vb = get(m2, b)
                if (op == 5 and va != 0) or (op == 6 and va == 0):
                    ip = vb
                else:
                    ip += 3
            elif op == 9:
                a = r(ip + 1)
                rb += get(m1, a)
                ip += 2
            else:
                raise ValueError(op)

        return outputs

    out1 = run([1])
    out2 = run([2])
    print(out1[-1] if out1 else 0)
    print(out2[-1] if out2 else 0)

if __name__ == '__main__':
    solve()
