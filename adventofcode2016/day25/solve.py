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

    def run_program(instructions, a_init, max_output=20):
        registers = {'a': a_init, 'b': 0, 'c': 0, 'd': 0}
        pc = 0
        output = []

        while pc < len(instructions) and len(output) < max_output:
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
            elif cmd == 'out':
                val = parts[1]
                if val.lstrip('-').isdigit():
                    output.append(int(val))
                else:
                    output.append(registers[val])
                pc += 1
            else:
                pc += 1

        return output

    # Find the lowest positive integer that produces alternating 0,1,0,1...
    for a in range(1, 1000):
        output = run_program(lines, a)
        expected = [i % 2 for i in range(len(output))]
        if output == expected and len(output) >= 10:
            part1 = a
            break

    print(f"Part 1: {part1}")

if __name__ == '__main__':
    solve()
