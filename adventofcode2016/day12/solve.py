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

    def run_program(instructions, registers):
        pc = 0
        while pc < len(instructions):
            parts = instructions[pc].split()
            cmd = parts[0]

            if cmd == 'cpy':
                src, dst = parts[1], parts[2]
                if src.lstrip('-').isdigit():
                    registers[dst] = int(src)
                else:
                    registers[dst] = registers[src]
                pc += 1
            elif cmd == 'inc':
                registers[parts[1]] += 1
                pc += 1
            elif cmd == 'dec':
                registers[parts[1]] -= 1
                pc += 1
            elif cmd == 'jnz':
                val = parts[1]
                if val.lstrip('-').isdigit():
                    test = int(val)
                else:
                    test = registers[val]

                if test != 0:
                    offset = int(parts[2])
                    pc += offset
                else:
                    pc += 1
            else:
                pc += 1

        return registers['a']

    # Part 1
    registers1 = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    part1 = run_program(lines, registers1)

    # Part 2
    registers2 = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
    part2 = run_program(lines, registers2)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
