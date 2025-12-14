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

    program = []
    for line in lines:
        if line:
            program = [int(x) for x in line.split(',')]
            break
    if not program:
        print(0)
        print(0)
        return

    def run(inp_val: int):
        mem = program[:]
        ip = 0
        outputs = []
        steps = 0
        max_steps = 50_000_000

        def get(mode, val):
            if mode == 0:
                return mem[val]
            if mode == 1:
                return val
            raise ValueError(mode)

        while True:
            steps += 1
            if steps > max_steps:
                raise RuntimeError(f"Intcode exceeded step limit at ip={ip}, instr={mem[ip]}")
            instr = mem[ip]
            op = instr % 100
            m1 = (instr // 100) % 10
            m2 = (instr // 1000) % 10

            if op == 99:
                break
            if op in (1, 2, 7, 8):
                a = mem[ip + 1]
                b = mem[ip + 2]
                c = mem[ip + 3]
                va = get(m1, a)
                vb = get(m2, b)
                if op == 1:
                    mem[c] = va + vb
                elif op == 2:
                    mem[c] = va * vb
                elif op == 7:
                    mem[c] = 1 if va < vb else 0
                else:
                    mem[c] = 1 if va == vb else 0
                ip += 4
            elif op == 3:
                a = mem[ip + 1]
                mem[a] = inp_val
                ip += 2
            elif op == 4:
                a = mem[ip + 1]
                outputs.append(get(m1, a))
                ip += 2
            elif op in (5, 6):
                a = mem[ip + 1]
                b = mem[ip + 2]
                va = get(m1, a)
                vb = get(m2, b)
                if (op == 5 and va != 0) or (op == 6 and va == 0):
                    ip = vb
                else:
                    ip += 3
            else:
                raise ValueError(op)

        return outputs

    out1 = run(1)
    out2 = run(5)
    print(out1[-1] if out1 else 0)
    print(out2[-1] if out2 else 0)

if __name__ == '__main__':
    solve()
