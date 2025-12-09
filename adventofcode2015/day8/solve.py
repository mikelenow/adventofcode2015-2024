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

    # Day 8: Matchsticks
    # Part 1: Difference between code length and in-memory length
    # Part 2: Difference between encoded length and code length

    total_code = 0
    total_memory = 0
    total_encoded = 0

    for line in lines:
        # Part 1: code vs memory
        total_code += len(line)
        # Evaluate the string literal to get actual memory size
        total_memory += len(eval(line))

        # Part 2: encode the string
        # Need to escape backslashes and quotes, then add outer quotes
        encoded = '"' + line.replace('\\', '\\\\').replace('"', '\\"') + '"'
        total_encoded += len(encoded)

    part1 = total_code - total_memory
    part2 = total_encoded - total_code

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == '__main__':
    solve()
