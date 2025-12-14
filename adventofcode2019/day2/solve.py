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

    def run(mem):
        ip = 0
        while True:
            op = mem[ip]
            if op == 99:
                return mem
            a, b, c = mem[ip + 1], mem[ip + 2], mem[ip + 3]
            if op == 1:
                mem[c] = mem[a] + mem[b]
            elif op == 2:
                mem[c] = mem[a] * mem[b]
            else:
                raise ValueError(op)
            ip += 4

    mem = program[:]
    mem[1] = 12
    mem[2] = 2
    part1 = run(mem)[0]

    target = 19690720
    part2 = None
    for noun in range(100):
        for verb in range(100):
            mem = program[:]
            mem[1] = noun
            mem[2] = verb
            out = run(mem)[0]
            if out == target:
                part2 = 100 * noun + verb
                break
        if part2 is not None:
            break

    print(part1)
    print(part2 if part2 is not None else 0)

if __name__ == '__main__':
    solve()
