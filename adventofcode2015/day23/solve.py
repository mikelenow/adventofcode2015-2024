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

    # Day 23: Opening the Turing Lock
    def run_program(a_init=0):
        registers = {'a': a_init, 'b': 0}
        pc = 0

        while 0 <= pc < len(lines):
            inst = lines[pc].split()
            cmd = inst[0]

            if cmd == 'hlf':
                registers[inst[1]] //= 2
                pc += 1
            elif cmd == 'tpl':
                registers[inst[1]] *= 3
                pc += 1
            elif cmd == 'inc':
                registers[inst[1]] += 1
                pc += 1
            elif cmd == 'jmp':
                pc += int(inst[1])
            elif cmd == 'jie':
                reg = inst[1].rstrip(',')
                if registers[reg] % 2 == 0:
                    pc += int(inst[2])
                else:
                    pc += 1
            elif cmd == 'jio':
                reg = inst[1].rstrip(',')
                if registers[reg] == 1:
                    pc += int(inst[2])
                else:
                    pc += 1

        return registers['b']

    part1 = run_program(0)
    part2 = run_program(1)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
