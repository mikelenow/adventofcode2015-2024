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

    # Day 7: Some Assembly Required
    # Simulate a circuit with bitwise logic gates

    def get_value(wire, wires, instructions):
        if wire.isdigit():
            return int(wire)

        if wire in wires:
            return wires[wire]

        instruction = instructions[wire]

        if 'AND' in instruction:
            parts = instruction.split(' AND ')
            result = get_value(parts[0], wires, instructions) & get_value(parts[1], wires, instructions)
        elif 'OR' in instruction:
            parts = instruction.split(' OR ')
            result = get_value(parts[0], wires, instructions) | get_value(parts[1], wires, instructions)
        elif 'LSHIFT' in instruction:
            parts = instruction.split(' LSHIFT ')
            result = get_value(parts[0], wires, instructions) << int(parts[1])
        elif 'RSHIFT' in instruction:
            parts = instruction.split(' RSHIFT ')
            result = get_value(parts[0], wires, instructions) >> int(parts[1])
        elif 'NOT' in instruction:
            wire_name = instruction.replace('NOT ', '')
            result = ~get_value(wire_name, wires, instructions) & 0xFFFF
        else:
            result = get_value(instruction, wires, instructions)

        wires[wire] = result
        return result

    # Part 1
    instructions = {}
    for line in lines:
        parts = line.split(' -> ')
        instructions[parts[1]] = parts[0]

    wires = {}
    part1 = get_value('a', wires, instructions)

    # Part 2: Override wire b with part1 result
    wires = {'b': part1}
    part2 = get_value('a', wires, instructions)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
