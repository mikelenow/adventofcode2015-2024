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

    def run_program(instructions, a_init):
        registers = {'a': a_init, 'b': 0, 'c': 0, 'd': 0}
        pc = 0
        instructions = [line.split() for line in instructions if line]

        while pc < len(instructions):
            cmd = instructions[pc]

            if cmd[0] == 'cpy':
                src, dst = cmd[1], cmd[2]
                if dst in registers:
                    if src.lstrip('-').isdigit():
                        registers[dst] = int(src)
                    elif src in registers:
                        registers[dst] = registers[src]
                pc += 1
            elif cmd[0] == 'inc':
                if cmd[1] in registers:
                    registers[cmd[1]] += 1
                pc += 1
            elif cmd[0] == 'dec':
                if cmd[1] in registers:
                    registers[cmd[1]] -= 1
                pc += 1
            elif cmd[0] == 'jnz':
                val = cmd[1]
                if val.lstrip('-').isdigit():
                    test = int(val)
                elif val in registers:
                    test = registers[val]
                else:
                    test = 0

                if test != 0:
                    offset = cmd[2]
                    if offset.lstrip('-').isdigit():
                        pc += int(offset)
                    elif offset in registers:
                        pc += registers[offset]
                    else:
                        pc += 1
                else:
                    pc += 1
            elif cmd[0] == 'tgl':
                offset = cmd[1]
                if offset in registers:
                    target = pc + registers[offset]
                else:
                    target = pc + int(offset)

                if 0 <= target < len(instructions):
                    target_cmd = instructions[target]
                    if len(target_cmd) == 2:
                        if target_cmd[0] == 'inc':
                            instructions[target] = ['dec', target_cmd[1]]
                        else:
                            instructions[target] = ['inc', target_cmd[1]]
                    elif len(target_cmd) == 3:
                        if target_cmd[0] == 'jnz':
                            instructions[target] = ['cpy', target_cmd[1], target_cmd[2]]
                        else:
                            instructions[target] = ['jnz', target_cmd[1], target_cmd[2]]
                pc += 1
            else:
                pc += 1

        return registers['a']

    part1 = run_program(lines, 7)
    part2 = run_program(lines, 12)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
